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

def print_info(info):
    print("  date %s" % info.answer["BatteryStatusRecords"]["OperationDateAndTime"])
    print("  date %s" % info.answer["BatteryStatusRecords"]["NotificationDateAndTime"])
    print("  battery_capacity2 %s" % info.answer["BatteryStatusRecords"]["BatteryStatus"]["BatteryCapacity"])
    print("  battery_capacity %s" % info.battery_capacity)
    print("  charging_status %s" % info.charging_status)
    print("  battery_capacity %s" % info.battery_capacity)
    print("  battery_remaining_amount %s" % info.battery_remaining_amount)
    print("  charging_status %s" % info.charging_status)
    print("  is_charging %s" % info.is_charging)
    print("  is_quick_charging %s" % info.is_quick_charging)
    print("  plugin_state %s" % info.plugin_state)
    print("  is_connected %s" % info.is_connected)
    print("  is_connected_to_quick_charger %s" % info.is_connected_to_quick_charger)
    print("  time_to_full_trickle %s" % info.time_to_full_trickle)
    print("  time_to_full_l2 %s" % info.time_to_full_l2)
    print("  time_to_full_l2_6kw %s" % info.time_to_full_l2_6kw)
    print("  battery_percent %s" % info.battery_percent)
    print("  state_of_charge %s" % info.state_of_charge)


# Main program
    
logging.debug("login = %s, password = %s, region = %s" % (username, password, region))

print("Prepare Session")
s = pycarwings2.Session(username, password, region)
print("Login...")
leaf = s.get_leaf()

print("get_latest_battery_status from servers")
leaf_info = leaf.get_latest_battery_status()
start_date = leaf_info.answer["BatteryStatusRecords"]["OperationDateAndTime"]
print("start_date=", start_date)
print_info(leaf_info)

print("request an update from the car itself")
result_key = leaf.request_update()
update_source = "";

while True:
    print("Waiting 10 seconds")
    time.sleep(10)  # sleep 60 seconds to give request time to process
    battery_status = leaf.get_status_from_update(result_key)
    # The Nissan Servers seem to have changed. Previously a battery_status would eventually be returned 
    # from get_status_from_update(), now this always seems to return 0.
    # Checking for updates via get_latest_battery_status() seems to be the way to check if an update
    # has been provided to the Nissan servers.
    if battery_status is None:
        print("No update, see latest_battery_status has changed")
        latest_leaf_info = leaf.get_latest_battery_status()
        latest_date = latest_leaf_info.answer["BatteryStatusRecords"]["OperationDateAndTime"]
        print("latest_date=", latest_date)
        if (latest_date != start_date):
            print("Latest info has updated we'll use that instead of waiting for get_status_from_update to respond")
            update_source = "get_latest_battery_status"
            break
    else:
        update_source = "get_status_from_update"
        break

if update_source == "get_status_from_update":
    pprint.pprint(battery_status.answer)
elif update_source == "get_latest_battery_status":
    print_info(latest_leaf_info)

exit()

# result_key = leaf.start_climate_control()
# time.sleep(60)
# start_cc_result = leaf.get_start_climate_control_result(result_key)

# result_key = leaf.stop_climate_control()
# time.sleep(60)
# stop_cc_result = leaf.get_stop_climate_control_result(result_key)
