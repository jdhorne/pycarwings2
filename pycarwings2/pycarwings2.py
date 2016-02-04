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

		log.info("invoking carwings API: %s" % req.url)
		log.debug("params: %s" % json.dumps(params, sort_keys=True, indent=3, separators=(',', ': ')))

		try:
			sess = requests.Session()
			response = sess.send(req)
			log.info('Response HTTP Status Code: {status_code}'.format(
				status_code=response.status_code))
			log.info('Response HTTP Response Body: {content}'.format(
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

	def get_leaf(self, index=0):
		return self.leaf


class Leaf:
	def __init__(self, session, vin, nickname):
		self.session = session
		self.vin = vin
		self.nickname = nickname
		log.debug("created leaf %s/%s" % (vin, nickname))

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
			return response

		return None

	def start_climate_control(self):
		pass

	def start_charging(self):
		pass
