#!/usr/bin/env python

import pycarwings2
import time

s = pycarwings2.Session("user@domain.com", "password")
l = s.get_leaf()
