# pycarwings2
Library for connecting and interacting with Nissan's CARWINGS service for Nissan LEAF cars.
Uses the (newly secure!) REST/JSON API rather than the previous XML-based API.

Inspired by original pycarwings library: https://github.com/haykinson/pycarwings

# asynchronous methods

Note that several of the most interesting methods in the CARWINGS service are
asynchronous--you ask the service to do something, and it just says "ok". You then
have to poll a corresponding method to find out if the operation was successful.

More details are located at the top of [pycarwings2.py](https://github.com/jdhorne/pycarwings2/blob/master/pycarwings2/pycarwings2.py).

# example usage

```python
import pycarwings2
import time

s = pycarwings2.Session("user@domain.com, "password")
l = s.get_leaf()

result_key = l.request_update()
time.sleep(60) # sleep 60 seconds to give request time to process
battery_status = l.get_status_from_update(result_key)

result_key = l.start_climate_control()
time.sleep(60)
start_cc_result = l.get_start_climate_control_result(result_key)

result_key = l.stop_climate_control()
time.sleep(60)
stop_cc_result = l.get_stop_climate_control_result(result_key)

```

# license
Copyright 2016 Jason Horne

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
