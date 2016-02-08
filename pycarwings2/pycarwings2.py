# Copyright 2016 Jason Horne
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from requests import Request, Session, RequestException
import json
import logging
from datetime import date

BASE_URL = "https://gdcportalgw.its-mo.com/orchestration_1111/gdc/"

log = logging.getLogger("pycarwings2")

class CarwingsError(Exception):
	pass

class Session(object):
	"""Maintains a connection to CARWINGS, refreshing it when needed"""

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.region_code = "NNA"
		self.logged_in = False

	def _request(self, endpoint, params):
		req = Request('GET', url=BASE_URL + endpoint, params=params).prepare()

		log.debug("invoking carwings API: %s" % req.url)
		log.debug("params: %s" % json.dumps(params, sort_keys=True, indent=3, separators=(',', ': ')))

		try:
			sess = requests.Session()
			response = sess.send(req)
			log.debug('Response HTTP Status Code: {status_code}'.format(
				status_code=response.status_code))
			log.debug('Response HTTP Response Body: {content}'.format(
				content=response.content))
		except RequestException:
			log.warning('HTTP Request failed')

		j = json.loads(response.content)

		if "ErrorMessage" in j:
			log.error("carwings error %s: %s" % (j["ErrorCode"], j["ErrorMessage"]) )
			raise CarwingsError

		return j

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
	def connect(self):
		response = self._request("UserLoginRequest.php", {
			"RegionCode": self.region_code,
			"UserId": self.username,
			"Password": self.password,
		})

		profile = response["vehicle"]["profile"]
		self.gdc_user_id = profile["gdcUserId"]
		log.debug("gdc_user_id: %s" % self.gdc_user_id)

		self.dcm_id = profile["dcmId"]
		log.debug("dcm_id: %s" % self.dcm_id)


		customer_info = response["CustomerInfo"]
		self.tz = customer_info["Timezone"]
		log.debug("tz: %s" % self.tz)
		self.language = customer_info["Language"]
		log.debug("language: %s" % self.language)

		vin = profile["vin"]
		log.debug("vin: %s" % vin)

		nickname = response["VehicleInfoList"]["vehicleInfo"][0]["nickname"]

		self.leaf = Leaf(self, vin, nickname)

		self.logged_in = True

	def get_leaf(self, index=0):
		if not self.logged_in:
			self.connect()

		return self.leaf


class Leaf:
	def __init__(self, session, vin, nickname):
		self.session = session
		self.vin = vin
		self.nickname = nickname
		log.debug("created leaf %s/%s" % (vin, nickname))

	"""
	example JSON response:
	{
		"status": 200,
		"message": "success",
		"userId": "user@domain.com",
		"vin": "1ABCDEFG2HIJKLM3N",
		"resultKey": "12345678901234567890123456789012345678901234567890"
	}
	"""
	def request_update(self):
		response = self.session._request("BatteryStatusCheckRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"UserId": self.session.gdc_user_id, # this userid is the 'gdc' userid
		})
		return response["resultKey"]

	"""
	example responses:

	not yet:
	{
		"status":200,
		"message":"success",
		"responseFlag":"0"
	}

	success:
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
	def get_status_from_update(self, result_key):
		response = self.session._request("BatteryStatusCheckResultRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"resultKey": result_key,
		})
		# responseFlag will be "1" if a response has been returned; "0" otherwise
		if response["responseFlag"] == "1":
			return response

		return None
	"""
	{
		"status":200,
		"message":"success",
		"userId":"user@domain.com",
		"vin":"1ABCDEFG2HIJKLM3N",
		"resultKey":"12345678901234567890123456789012345678901234567890"
	}
	"""
	def start_climate_control(self):
		response = self.session._request("ACRemoteRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		return response["resultKey"]

	"""
	not yet:
	{
		"status":200,
		"message":"success",
		"responseFlag":"0"
	}
	success:
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
	# response will have:
	#	"hvacStatus": "ON" or "OFF"
	#   "operationResult": "START_BATTERY" or ...?
	#   "acContinueTime": e.g. "15"
	def get_start_climate_control_result(self, result_key):
		response = self.session._request("ACRemoteResult.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"UserId": self.session.gdc_user_id, # this userid is the 'gdc' userid
			"resultKey": result_key,
		})
		if response["responseFlag"] == "1":

			# seems to indicate that the vehicle cannot be reached
			if response["operationResult"] == "ELECTRIC_WAVE_ABNORMAL":
				log.warning("could not establish communications with vehicle")
				raise CarwingsError("could not establish communications with vehicle")

			return response

		return None
	"""
	sample JSON response:
	{
		"status":200,
		"message":"success",
		"userId":"user@domain.com",
		"vin":"1ABCDEFG2HIJKLM3N",
		"resultKey":"12345678901234567890123456789012345678901234567890"
	}
	"""
	def stop_climate_control(self):
		response = self.session._request("ACRemoteOffRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		return response["resultKey"]

	"""
	not yet:
	{
		"status":200,
		"message":"success",
		"responseFlag":"0"
	}

	success:
	"""
	# response will have:
	#	"hvacStatus": "ON" or "OFF"
	def get_stop_climate_control_result(self, result_key):
		response = self.session._request("ACRemoteOffResult.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"UserId": self.session.gdc_user_id, # this userid is the 'gdc' userid
			"resultKey": result_key,
		})
		if response["responseFlag"] == "1":
			return response

		return None

	"""
	{
		"status":200,
		"message":"success"
	}
	"""
	def start_charging(self):
		response = self.session._request("BatteryRemoteChargingRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"ExecuteTime": date.today().isoformat()
		})
		if response["status"] == "success":
			return True

		return False
