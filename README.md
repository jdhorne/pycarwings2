# pycarwings2

Library for connecting and interacting with Nissan's CARWINGS service for Nissan LEAF cars.
Uses the (newly secure!) REST/JSON API rather than the previous XML-based API.

Inspired by original pycarwings library: https://github.com/haykinson/pycarwings

## Asynchronous methods

Note that several of the most interesting methods in the CARWINGS service are
asynchronous--you ask the service to do something, and it just says "ok". You then
have to poll a corresponding method to find out if the operation was successful.

More details are located at the top of [pycarwings2.py](https://github.com/filcole/pycarwings2/blob/HomeAssistant/pycarwings2/pycarwings2.py).

## Installation

    pip3 install requests pycryptodome configparser
    pip3 install git+https://github.com/filcole/pycarwings2.git HomeAssistant

## Example usage

./examples/get-leaf-info.py

## License

Copyright 2016 Jason Horne
Copyright 2018 Phil Cole

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
