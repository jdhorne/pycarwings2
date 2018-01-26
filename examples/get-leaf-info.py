#!/usr/bin/python

import pycarwings2
import time
from ConfigParser import SafeConfigParser
import logging
import sys
import pprint

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


parser = SafeConfigParser()
candidates = ['config.ini', 'my_config.ini']
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

logging.debug("login = %s , password = %s" % (username, password))

print "Prepare Session"
s = pycarwings2.Session(username, password, "NE")
print "Login..."
l = s.get_leaf()

print "get_latest_battery_status"
leaf_info = l.get_latest_battery_status()
print "date %s" % leaf_info.answer["BatteryStatusRecords"]["OperationDateAndTime"]
print "date %s" % leaf_info.answer["BatteryStatusRecords"]["NotificationDateAndTime"]
print "battery_capacity2 %s" % leaf_info.answer["BatteryStatusRecords"]["BatteryStatus"]["BatteryCapacity"]

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
print "leaf_info.state_of_charge %s" % leaf_info.state_of_charge


result_key = l.request_update()
print "start sleep 10"
time.sleep(10)  # sleep 60 seconds to give request time to process
print "end sleep 10"
battery_status = l.get_status_from_update(result_key)
while battery_status is None:
    print "not update"
    time.sleep(10)
    battery_status = l.get_status_from_update(result_key)

pprint.pprint(battery_status.answer)

# result_key = l.start_climate_control()
# time.sleep(60)
# start_cc_result = l.get_start_climate_control_result(result_key)

# result_key = l.stop_climate_control()
# time.sleep(60)
# stop_cc_result = l.get_stop_climate_control_result(result_key)
