#!/usr/bin/env python

import pycarwings2
from configparser import ConfigParser
import logging
import sys

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

print("get_latest_hvac_status from servers")
leaf_info = leaf.get_latest_hvac_status()
if leaf_info.is_hvac_running:
    print("Climate control is on")
else:
    print("Climate control is off")
