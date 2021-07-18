# pycarwings2

[![Build Status](https://travis-ci.com/filcole/pycarwings2.svg?branch=master)](https://travis-ci.com/filcole/pycarwings2)

Python3 version of the pycarwings2 library.

Library for connecting and interacting with Nissan's CARWINGS service for Nissan LEAF cars.
Uses the (newly secure!) REST/JSON API rather than the previous XML-based API.

Note: The US may use an entirely RESTful API as mentioned in [this gist by BenWoodford](https://gist.github.com/BenWoodford/141ca350445e994e69a70aabfb6db942) and [Issue 30](https://github.com/jdhorne/pycarwings2/issues/30)  Please report if this works in the US.  I am based in the UK.

Inspired by original pycarwings library: https://github.com/haykinson/pycarwings including code from https://github.com/jdhorne/pycarwings2 and https://github.com/BenWoodford/pycarwings2

## Asynchronous methods

Note that several of the most interesting methods in the CARWINGS service are
asynchronous--you ask the service to do something, and it just says "ok". You then
have to poll a corresponding method to find out if the operation was successful.

Recently the polling has continued to return zero, yet when querying the data
held on the Nissan servers the last update date changes, indicating a response
has been received from the car, see examples/get-leaf-info.py for how this can
be handled.

More details are located at the top of [pycarwings2.py](https://github.com/filcole/pycarwings2/blob/HomeAssistant/pycarwings2/pycarwings2.py).

## Installation

    pip3 install pycarwings2

## Example usage

* Copy file ./examples/config.ini to ./examples/my_config.ini
* Edit my_config.ini and enter your username, password and region
* Run python3 ./examples/get-leaf-info.py

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
