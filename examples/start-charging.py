#!/usr/bin/env python

import pycarwings2
import time
from configparser import ConfigParser
import logging
import sys
import pprint

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

parser = ConfigParser()
candidates = ['config.ini', 'my_config.ini']
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')
region = parser.get('get-leaf-info', 'region')

# Main program

logging.debug("login = %s, password = %s, region = %s" % (username, password, region))

print("Prepare Session")
s = pycarwings2.Session(username, password, region)
print("Login...")
leaf = s.get_leaf()

print("Starting Charge...")
if leaf.start_charging():
    # Note that the car may not even be plugged in, but it will still accept
    # a "start charging" command.  To confirm charging check the battery status.
    print("Command Sent Successfully")
else:
    print("Failed")

exit()
