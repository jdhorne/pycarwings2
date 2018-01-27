#!/usr/bin/env python

import pycarwings2
from configparser import ConfigParser
import logging
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


parser = SafeConfigParser()
candidates = ['config.ini', 'my_config.ini']
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s , password = %s" % (username, password))

print("Prepare Session")
s = pycarwings2.Session(username, password, "NE")
print("Login...")
leaf = s.get_leaf()

print("request_location")

result_key = leaf.request_location()

while True:
    location_status = leaf.get_status_from_location(result_key)
    if location_status is None:
        print("Waiting for response (sleep 10)")
        time.sleep(10)
    else:
        print("lat: {} long: {}".format(location_status.latitude, location_status.longitude))
        break
