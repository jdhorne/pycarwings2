#!/usr/bin/python

import sys
sys.path.append('/home/ruben/pycarwings2/pycarwings2')

import pycarwings3
import time
from ConfigParser import SafeConfigParser
import logging
import sys
import pprint

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


parser = SafeConfigParser()
candidates = [ 'config.ini', 'my_config.ini' ]
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s , password = %s" % ( username , password)  )

print "Prepare Session"
s = pycarwings3.Session(username, password , "NE")
print "Login..."
l = s.get_leaf()

print "request_location"

result_key = l.request_location()
print "start sleep 60"
time.sleep(60) # sleep 60 seconds to give request time to process
print "end sleep 60"
location_status = l.get_status_from_location(result_key)
print(location_status)
