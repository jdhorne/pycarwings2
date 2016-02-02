import requests

class Session(object):
	"""Maintains a connection to CARWINGS, refreshing it when needed"""

	def __init__(self, username, password, region="US"):
		self.username = username
		self.password = password
		self.logged_in = False
		self.set_region(region)
		self.connect()

	def set_region(self, r):
		pass

	def connect(self):
		# Carwings Login
		# GET https://gdcportalgw.its-mo.com/orchestration_1111/gdc/UserLoginRequest.php

		try:
			response = requests.get(
				url="https://gdcportalgw.its-mo.com/orchestration_1111/gdc/UserLoginRequest.php",
				params={
					"RegionCode": "NNA",
					"lg": "en-US",
					"DCMID": "",
					"VIN": "",
					"tz": "",
					"UserId": self.username,
					"Password": self.password,
				},
			)
			print('Response HTTP Status Code: {status_code}'.format(
			status_code=response.status_code))
			print('Response HTTP Response Body: {content}'.format(
			content=response.content))
		except requests.exceptions.RequestException:
			print('HTTP Request failed')
