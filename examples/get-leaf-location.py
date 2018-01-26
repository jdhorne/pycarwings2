#!/usr/bin/python

#import sys
#sys.path.append('/home/ruben/leaf/pycarwings2/pycarwings2')

import pycarwings2
import time
from ConfigParser import SafeConfigParser
import logging
import sys
import pprint

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


parser = SafeConfigParser()
candidates = [ 'config.ini', 'my_config.ini' ]
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s , password = %s" % ( username , password)  )

print "Prepare Session"
s = pycarwings2.Session(username, password , "NE")
print "Login..."
l = s.get_leaf()

print "request_location"

result_key = l.request_location()

while True:
	location_status = l.get_status_from_location(result_key)
	if location_status is None:
		print "Waiting for response (sleep 10)"
		time.sleep(10)
	else:
		print("lat: {} long: {}".format(location_status.latitude, location_status.longitude))
		break
