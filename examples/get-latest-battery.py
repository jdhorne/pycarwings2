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
