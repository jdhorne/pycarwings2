#!/usr/bin/env python

import pycarwings2
import logging
import sys
from configparser import ConfigParser

if len(sys.argv) < 2:
    print("Need input either 'start' or 'stop' as argument")
    exit()

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

# Put in username and path to your log-file.

parser = ConfigParser()
candidates = ['config.ini', 'my_config.ini']
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')
region = parser.get('get-leaf-info', 'region')

logging.debug("login = %s, password = %s, region = %s" % (username, password, region))

print("Prepare Session")
s = pycarwings2.Session(username, password, region)
print("Login...")
leaf = s.get_leaf()

if str.lower(sys.argv[1]) == 'start':
    print("Starting climate control")
    result_key = leaf.start_climate_control()

if str.lower(sys.argv[1]) == 'stop':
    print("Stopping climate control")
    result_key = leaf.stop_climate_control()
