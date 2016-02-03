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

print("sleeping for 30 seconds")
time.sleep(30)

l.get_status_from_update(result_key)
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
