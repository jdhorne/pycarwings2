import logging
from datetime import date, timedelta, datetime

log = logging.getLogger("pycarwings2")

CONNECTED_VALUE_MAP = {
	'CONNECTED': True,
	'NOT_CONNECTED'  : False
}

def _time_remaining(t):
	minutes = float(0)
	if t:
		if t["hours"]:
			minutes = float(60*t["hours"])
		if t["minutes"]:
			minutes += t["minutes"]
	return minutes


class CarwingsResponse:
	def _set_cruising_ranges(self, status):
		self.cruising_range_ac_off_km = float(status["cruisingRangeAcOff"]) / 1000
		self.cruising_range_ac_on_km = float(status["cruisingRangeAcOn"]) / 1000

	def _set_timestamp(self, status):
		self.timestamp = datetime.strptime(status["timeStamp"], "%Y-%m-%d %H:%M:%S") # "2016-01-02 17:17:38"

	"""
	example JSON response to login:

	{
		"status":200,
		"message":"success",
		"sessionId":"12345678-1234-1234-1234-1234567890",
		"VehicleInfoList": {
			"VehicleInfo": [
				{
					"charger20066":"false",
					"nickname":"LEAF",
					"telematicsEnabled":"true",
					"vin":"1ABCDEFG2HIJKLM3N"
				}
			],
			"vehicleInfo": [
				{
					"charger20066":"false",
					"nickname":"LEAF",
					"telematicsEnabled":"true",
					"vin":"1ABCDEFG2HIJKLM3N"
				}
			]
		},
		"vehicle": {
			"profile": {
				"vin":"1ABCDEFG2HIJKLM3N",
				"gdcUserId":"FG12345678",
				"gdcPassword":"password",
				"encAuthToken":"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",
				"dcmId":"123456789012",
				"nickname":"Alpha124",
				"status":"ACCEPTED",
				"statusDate": "Aug 15, 2015 07:00 PM"
			}
		},
		"EncAuthToken":"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",
		"CustomerInfo": {
			"UserId":"AB12345678",
			"Language":"en-US",
			"Timezone":"America\/New_York",
			"RegionCode":"NNA",
			"OwnerId":"1234567890",
			"Nickname":"Bravo456",
			"Country":"US",
			"VehicleImage":"\/content\/language\/default\/images\/img\/ph_car.jpg",
			"UserVehicleBoundDurationSec":"999971200",
			"VehicleInfo": {
				"VIN":"1ABCDEFG2HIJKLM3N",
				"DCMID":"201212345678",
				"SIMID":"12345678901234567890",
				"NAVIID":"1234567890",
				"EncryptedNAVIID":"1234567890ABCDEFGHIJKLMNOP",
				"MSN":"123456789012345",
				"LastVehicleLoginTime":"",
				"UserVehicleBoundTime":"2015-08-17T14:16:32Z",
				"LastDCMUseTime":""
			}
		},
		"UserInfoRevisionNo":"1"
	}
	"""
class CarwingsLoginResponse(CarwingsResponse):
	def __init__(self, response):
		profile = response["vehicle"]["profile"]
		self.gdc_user_id = profile["gdcUserId"]
		self.dcm_id = profile["dcmId"]
		self.vin = profile["vin"]

		self.nickname = response["VehicleInfoList"]["vehicleInfo"][0]["nickname"]

		customer_info = response["CustomerInfo"]
		self.tz = customer_info["Timezone"]
		self.language = customer_info["Language"]

		self.leafs = [ { "vin": self.vin, "nickname": self.nickname } ]



"""
	{
		"status": 200,
		"message": "success",
		"responseFlag": "1",
		"operationResult": "START",
		"timeStamp": "2016-01-02 17:17:38",
		"cruisingRangeAcOn": "115328.0",
		"cruisingRangeAcOff": "117024.0",
		"currentChargeLevel": "0",
		"chargeMode": "220V",
		"pluginState": "CONNECTED",
		"charging": "YES",
		"chargeStatus": "CT",
		"batteryDegradation": "10",
		"batteryCapacity": "12",
		"timeRequiredToFull": {
			"hours": "",
			"minutes": ""
		},
		"timeRequiredToFull200": {
			"hours": "",
			"minutes": ""
		},
		"timeRequiredToFull200_6kW": {
			"hours": "",
			"minutes": ""
		}
	}
"""
class CarwingsBatteryStatusResponse(CarwingsResponse):
	def __init__(self, status):
		self._set_timestamp(status)
		self._set_cruising_ranges(status)

		self.battery_capacity = status["batteryCapacity"]
		self.battery_degradation = status["batteryDegradation"]

		try:
			self.is_connected = CONNECTED_VALUE_MAP[status["pluginState"]]
		except KeyError:
			log.error(u"Unknown connected state: '%s'" % status["pluginState"])
			self.is_connected = True # probably

		self.charging_status = status["chargeMode"]

		self.is_charging = ("YES" == status["charging"])

		self.time_to_full_trickle = timedelta(minutes=_time_remaining(status["timeRequiredToFull"]))
		self.time_to_full_l2 = timedelta(minutes=_time_remaining(status["timeRequiredToFull200"]))
		self.time_to_full_l2_6kw = timedelta(minutes=_time_remaining(status["timeRequiredToFull200_6kW"]))

		self.battery_percent = 100 * float(status["batteryDegradation"]) / float(status["batteryCapacity"])

"""
	{
		"status":200,
		"message":"success",
		"responseFlag":"1",
		"operationResult":"START_BATTERY",
		"acContinueTime":"15",
		"cruisingRangeAcOn":"106400.0",
		"cruisingRangeAcOff":"107920.0",
		"timeStamp":"2016-02-05 12:59:46",
		"hvacStatus":"ON"
	}
"""
class CarwingsStartClimateControlResponse(CarwingsResponse):
	def __init__(self, status):
		self._set_timestamp(status)
		self._set_cruising_ranges(status)

		self.operation_result = status["operationResult"] # e.g. "START_BATTERY", ...?
		self.ac_continue_time = timedelta(minutes=float(status["acContinueTime"]))
		self.hvac_status = status["hvacStatus"]  # "ON" or "OFF"
		self.is_hvac_running = ("ON" == self.hvac_status)
"""
	{
		"status":200,
		"message":"success",
		"responseFlag":"1",
		"operationResult":"START",
		"timeStamp":"2016-02-09 03:32:51",
		"hvacStatus":"OFF"
	}
"""
class CarwingsStopClimateControlResponse(CarwingsResponse):
	def __init__(self, status):
		self._set_timestamp(status)
		self.hvac_status = status["hvacStatus"]  # "ON" or "OFF"
		self.is_hvac_running = ("ON" == self.hvac_status)
