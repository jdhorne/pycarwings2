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
	pass

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
		self.timestamp = datetime.strptime(status["timeStamp"], "%Y-%m-%d %H:%M:%S") # "2016-01-02 17:17:38"

		self.battery_capacity = status["batteryCapacity"]
		self.battery_degradation = status["batteryDegradation"]

		try:
			self.is_connected = CONNECTED_VALUE_MAP[status["pluginState"]]
		except KeyError:
			log.error(u"Unknown connected state: '%s'" % status["pluginState"])
			self.is_connected = True # probably

		self.cruising_range_ac_off_km = float(status["cruisingRangeAcOff"]) / 1000
		self.cruising_range_ac_on_km = float(status["cruisingRangeAcOn"]) / 1000
		self.charging_status = status["chargeMode"]

		self.is_charging = ("YES" == status["charging"])

		self.time_to_full_trickle = timedelta(minutes=_time_remaining(status["timeRequiredToFull"]))
		self.time_to_full_trickle_l2 = timedelta(minutes=_time_remaining(status["timeRequiredToFull200"]))
		self.time_to_full_trickle_l2_6kw = timedelta(minutes=_time_remaining(status["timeRequiredToFull200_6kW"]))

		self.battery_percent = 100 * float(status["batteryDegradation"]) / float(status["batteryCapacity"])
