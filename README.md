# python-dash-robot

An unofficial (and unsanctioned) python library for controlling
[Wonder Workshop's](https://www.makewonder.com/)
[Dash](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) robot.

## NOTICE:
Adapted from original source code Copyright 2016 Ilya Sukhanov
distributed under Apache 2.0 license
https://github.com/IlyaSukhanov/morseapi

Key differences:
- Adapted to support Python 3.x
- Removed references to GenericRobot
- Added function to get Dash by device name
- Dockerfile
- Sensors are not yet supported
- Dot is not supported

## Motivation
The motivation for this work was primarily to provide a platform to explore Python coding with my kids.  The opportunity to experiment with Bluetooth LE was also a factor.

## Compatibility
Docker container and source code work when deployed under Ubuntu 18.04.  Not tested on other platforms.

## Getting Started
Running docker container on host network will launch CPython interpreter:
```
docker run -it --net=host --name=dash havnfun/python-dash-robot
```
Import library:
```Python
>>> from dash import robot
```
Create an instance of the robot and play:
```Python
>>> dash = robot.robot(robot.get_dash())
Found Dash at: XX:XX:XX:XX:XX:XX
Connecting to: XX:XX:XX:XX:XX:XX
Connecting to: <pygatt.backends.gatttool.device.GATTToolBLEDevice object at ... >
>>> dash.say('hi')
```
(Note that additional warnings are displayed when running in Docker.)
