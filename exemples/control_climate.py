#!/usr/bin/python

import pycarwings2
import time
import logging
import sys
from datetime import datetime

if len(sys.argv) < 2:
    print "Need input either 'start' or 'stop' as argument"
    exit()

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

# Put in username and path to your log-file.

username = "username@dot.com"
password = "xxxxxx"
path = "/home/pi/scripts/"

##

logging.debug("login = %s , password = %s" % (username, password))

print "Prepare Session"
s = pycarwings2.Session(username, password, "NE")
print "Login..."
l = s.get_leaf()

if str.lower(sys.argv[1]) == 'start':
    print "Starting climate control"
    result_key = l.start_climate_control()

if str.lower(sys.argv[1]) == 'stop':
    print "Stopping climate control"
    result_key = l.stop_climate_control()

with open(path + 'climate_control.log', 'a') as file:
    file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
               ',' + str.lower(sys.argv[1]) + '\n')
