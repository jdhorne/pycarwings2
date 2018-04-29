#!/usr/bin/env python

#import sys
# sys.path.append('/home/ruben/leaf/pycarwings2/pycarwings2')

import pycarwings2
from configparser import ConfigParser
import logging
import sys
import time


logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

parser = ConfigParser()
candidates = ['config.ini', 'my_config.ini']
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s, password = %s" % (username, password))

print("Prepare Session")
session = pycarwings2.Session(username, password, "NE")
print("Login...")
leaf = session.get_leaf()

print("request_location")

result_key = leaf.request_location()

while True:
    location_status = leaf.get_status_from_location(result_key)
    if location_status is None:
        print("Waiting for response (sleep 10)")
        time.sleep(10)
    else:
        lat = location_status.latitude
        lon = location_status.longitude
        print("lat: {} long: {}".format(lat, lon))
        # OpenStreetMap url, ctrl click in terminal to open browser,
        # for example, my parking lot ;)
        # http://www.openstreetmap.org/search?query=52.37309+4.89217#map=19/52.37310/4.89220
        z = 19 # zoom level, lower is bigger area
        print("http://www.openstreetmap.org/search?query={}%20{}#map={}/{}/{}".format(lat,lon,z,lat,lon))
        break
