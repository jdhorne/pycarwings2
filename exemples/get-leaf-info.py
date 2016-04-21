#!/usr/bin/python

import pycarwings2.pycarwings2
import time
from ConfigParser import SafeConfigParser
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


parser = SafeConfigParser()
candidates = [ 'config.ini', 'my_config.ini' ]
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s , password = %s" % ( username , password)  )

s = pycarwings2.pycarwings2.Session(username, password , "NE")
l = s.get_leaf()

leaf_info = l.get_latest_battery_status()
print "battery_capacity %s" % leaf_info.battery_capacity
print "charging_status %s" % leaf_info.charging_status
print "battery_capacity %s" % leaf_info.battery_capacity
print "battery_remaining_amount %s" % leaf_info.battery_remaining_amount
print "charging_status %s" % leaf_info.charging_status
print "is_charging %s" % leaf_info.is_charging
print "is_quick_charging %s" % leaf_info.is_quick_charging
print "plugin_state %s" % leaf_info.plugin_state
print "is_connected %s" % leaf_info.is_connected
print "is_connected_to_quick_charger %s" % leaf_info.is_connected_to_quick_charger
print "time_to_full_trickle %s" % leaf_info.time_to_full_trickle
print "time_to_full_l2 %s" % leaf_info.time_to_full_l2
print "time_to_full_l2_6kw %s" % leaf_info.time_to_full_l2_6kw
print "leaf_info.battery_percent %s" % leaf_info.battery_percent

#time.sleep(60) # sleep 60 seconds to give request time to process
#battery_status = l.get_status_from_update(result_key)
#print "Battery Status"
#print battery_status

#result_key = l.start_climate_control()
#time.sleep(60)
#start_cc_result = l.get_start_climate_control_result(result_key)

#result_key = l.stop_climate_control()
#time.sleep(60)
#stop_cc_result = l.get_stop_climate_control_result(result_key)
