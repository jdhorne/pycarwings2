#!/usr/bin/env python

import logging
import sys
import pytest
import pycarwings2

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def test_bad_password():
    with pytest.raises(pycarwings2.responses.CarwingsError) as excinfo:
        s = pycarwings2.Session("user@domain.com", "password", "NE")
        leaf = s.get_leaf()
        if leaf is not None:
            pass
        assert 'INVALID' in str(excinfo.value)
