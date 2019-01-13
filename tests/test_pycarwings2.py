#!/usr/bin/env python

import logging
import sys
import pytest
from pycarwings2 import Session, CarwingsError

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def test_bad_password():
    with pytest.raises(CarwingsError) as excinfo:
        s = Session("user@domain.com", "password", "NE")
        leaf = s.get_leaf()
        if leaf is not None:
            pass
    assert 'INVALID' in str(excinfo.value)
