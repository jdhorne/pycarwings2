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

"""
There are three asynchronous operations in this API, paired with three follow-up
"status check" methods.

	request_update           -> get_status_from_update
	start_climate_control    -> get_start_climate_control_result
	stop_climate_control     -> get_stop_climate_control_result

The asynchronous operations immediately return a 'result key', which
is then supplied as a parameter for the corresponding status check method.

Here's an example response from an asynchronous operation, showing the result key:

	{
		"status":200,
		"message":"success",
		"userId":"user@domain.com",
		"vin":"1ABCDEFG2HIJKLM3N",
		"resultKey":"12345678901234567890123456789012345678901234567890"
	}

The status check methods return a JSON blob containing a 'responseFlag' property.
If the communications are complete, the response flag value will be the string "1";
otherwise the value will be the string "0". You just gotta poll until you get a
"1" back. Note that the official app seems to poll every 20 seconds.

Example 'no response yet' result from a status check invocation:

	{
		"status":200,
		"message":"success",
		"responseFlag":"0"
	}

When the responseFlag does come back as "1", there will also be an "operationResult"
property. If there was an error communicating with the vehicle, it seems that
this field will contain the value "ELECTRIC_WAVE_ABNORMAL". Odd.

"""

import requests
from requests import Request, Session, RequestException
import json
import logging
from datetime import date
from responses import *

BASE_URL = "https://gdcportalgw.its-mo.com/orchestration_1111/gdc/"

log = logging.getLogger("pycarwings2")

class CarwingsError(Exception):
	pass

class Session(object):
	"""Maintains a connection to CARWINGS, refreshing it when needed"""

	def __init__(self, username, password, region="NNA"):
		self.username = username
		self.password = password
		self.region_code = region
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

	def connect(self):
		response = self._request("UserLoginRequest.php", {
			"RegionCode": self.region_code,
			"UserId": self.username,
			"Password": self.password,
		})

		ret = CarwingsLoginResponse(response)

		self.gdc_user_id = ret.gdc_user_id
		log.debug("gdc_user_id: %s" % self.gdc_user_id)
		self.dcm_id = ret.dcm_id
		log.debug("dcm_id: %s" % self.dcm_id)
		self.tz = ret.tz
		log.debug("tz: %s" % self.tz)
		self.language = ret.language
		log.debug("language: %s" % self.language)
		log.debug("vin: %s" % ret.vin)
		log.debug("nickname: %s" % ret.nickname)

		self.leaf = Leaf(self, ret.leafs[0])

		self.logged_in = True

		return ret

	def get_leaf(self, index=0):
		if not self.logged_in:
			self.connect()

		return self.leaf


class Leaf:
	def __init__(self, session, params):
		self.session = session
		self.vin = params["vin"]
		self.nickname = params["nickname"]
		self.bound_time = params["bound_time"]
		log.debug("created leaf %s/%s" % (self.vin, self.nickname))

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
			return CarwingsBatteryStatusResponse(response)

		return None

	def start_climate_control(self):
		response = self.session._request("ACRemoteRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		return response["resultKey"]

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

			return CarwingsStartClimateControlResponse(response)

		return None

	def stop_climate_control(self):
		response = self.session._request("ACRemoteOffRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		return response["resultKey"]

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
			return CarwingsStopClimateControlResponse(response)

		return None

	# execute time example: "2016-02-09 17:24"
	# I believe this time is specified in GMT, despite the "tz" parameter
	# TODO: change parameter to python datetime object(?)
	def schedule_climate_control(self, execute_time):
		response = self.session._request("ACRemoteNewRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"ExecuteTime": execute_time,
		})
		return (response["message"] == "success")

	# execute time example: "2016-02-09 17:24"
	# I believe this time is specified in GMT, despite the "tz" parameter
	# TODO: change parameter to python datetime object(?)
	def update_scheduled_climate_control(self, execute_time):
		response = self.session._request("ACRemoteUpdateRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"ExecuteTime": execute_time,
		})
		return (response["message"] == "success")

	def cancel_scheduled_climate_control(self):
		response = self.session._request("ACRemoteCancelRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		return (response["message"] == "success")

	def get_climate_control_schedule(self):
		response = self.session._request("GetScheduledACRemoteRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		if (response["message"] == "success"):
			if response["ExecuteTime"] != "":
				return CarwingsClimateControlScheduleResponse(response)

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

	def get_driving_analysis(self):
		response = self.session._request("DriveAnalysisBasicScreenRequestEx.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
		})
		if response["message"] == "success":
			return CarwingsDrivingAnalysisResponse(response)

		return None

	def get_latest_battery_status(self):
		response = self.session._request("BatteryStatusRecordsRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"TimeFrom": self.bound_time
		})
		if response["message"] == "success":
			return CarwingsLatestBatteryStatusResponse(response)

		return None

	# target_month format: "YYYYMM" e.g. "201602"
	def get_electric_rate_simulation(self, target_month):
		response = self.session._request("PriceSimulatorDetailInfoRequest.php", {
			"RegionCode": self.session.region_code,
			"lg": self.session.language,
			"DCMID": self.session.dcm_id,
			"VIN": self.vin,
			"tz": self.session.tz,
			"TargetMonth": target_month
		})
		if response["message"] == "success":
			return CarwingsElectricRateSimulationResponse(response)

		return None
