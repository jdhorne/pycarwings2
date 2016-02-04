# pycarwings2
Library for connecting and interacting with Nissan's CARWINGS service for Nissan LEAF cars.
Uses the REST/JSON API rather than the previous XML-based API.

Inspired by original pycarwings library: https://github.com/haykinson/pycarwings

# example usage

```python
import pycarwings2
import time

s = pycarwings2.Session("user@domain.com, "password")
l = s.get_leaf()

result_key = l.request_update()
time.sleep(60) # sleep 60 seconds to give request time to process
l.get_status_from_update(result_key)

result_key = l.start_climate_control()
time.sleep(60)
l.get_start_climate_control_result(result_key)

result_key = l.stop_climate_control()
time.sleep(60)
l.get_stop_climate_control_result(result_key)

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
