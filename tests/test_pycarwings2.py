#!/usr/bin/env python

import json
import logging
import sys
import pytest
from pycarwings2 import Session, CarwingsError
from pycarwings2.responses import CarwingsLatestClimateControlStatusResponse

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def test_bad_password():
    with pytest.raises(CarwingsError) as excinfo:
        s = Session("user@domain.com", "password", "NE")
        leaf = s.get_leaf()
        if leaf is not None:
            pass
    assert 'INVALID' in str(excinfo.value)


def test_get_latest_hvac_status_on():
    # Source: original pycarwings2 sources
    climateresponse = """
        {
            "status":200,
            "message":"success",
            "RemoteACRecords":{
                "OperationResult":"START_BATTERY",
                "OperationDateAndTime":"Feb 10, 2016 10:22 PM",
                "RemoteACOperation":"START",
                "ACStartStopDateAndTime":"Feb 10, 2016 10:23 PM",
                "CruisingRangeAcOn":"107712.0",
                "CruisingRangeAcOff":"109344.0",
                "ACStartStopURL":"",
                "PluginState":"NOT_CONNECTED",
                "ACDurationBatterySec":"900",
                "ACDurationPluggedSec":"7200"
            },
            "OperationDateAndTime":""
        }
"""
    response = json.loads(climateresponse)
    status = CarwingsLatestClimateControlStatusResponse(response)
    assert status.is_hvac_running


def test_get_latest_hvac_status_off():
    # Source: From 24kWh Leaf (Climate is OFF)
    climateresponse = """
{"status":200,"RemoteACRecords":{"OperationResult":"START_BATTERY","OperationDateAndTime":"11-Jan-2019 17:51","RemoteACOperation":"STOP","ACStartStopDateAndTime":"2019/01/11 16:52","CruisingRangeAcOn":"74328.0","CruisingRangeAcOff":"79544.0","ACStartStopURL":"","PluginState":"NOT_CONNECTED","ACDurationBatterySec":"900","ACDurationPluggedSec":"7200"}}
"""
    response = json.loads(climateresponse)
    status = CarwingsLatestClimateControlStatusResponse(response)
    assert not status.is_hvac_running


def test_get_latest_hvac_status_error():
    # Source: original pycarwings2 sources
    climateresponse = """
        {
            "status":200,
            "RemoteACRecords":{
                "OperationResult":"ELECTRIC_WAVE_ABNORMAL",
                "OperationDateAndTime":"2018/04/08 10:00",
                "RemoteACOperation":"START",
                "ACStartStopDateAndTime":"08-Apr-2018 11:06",
                "ACStartStopURL":"",
                "PluginState":"INVALID",
                "ACDurationBatterySec":"900",
                "ACDurationPluggedSec":"7200",
                "PreAC_unit":"C",
                "PreAC_temp":"22"
            }
        }
"""
    # Assume climate control is off if we get back an empty response
    response = json.loads(climateresponse)
    with pytest.raises(CarwingsError) as excinfo:
        CarwingsLatestClimateControlStatusResponse(response)
        assert 'Should have exception here'

    assert 'could not establish communications with vehicle' in str(excinfo.value)


def test_get_latest_hvac_status_empty():
    # Source: 30kWh Leaf as at 13/01/2019
    climateresponse = """
{"status":200,"RemoteACRecords":[]}
"""
    # Assume climate control is off if we get back an empty response
    response = json.loads(climateresponse)
    status = CarwingsLatestClimateControlStatusResponse(response)
    assert not status.is_hvac_running
