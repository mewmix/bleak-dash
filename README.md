# bleak-dash

An unofficial [bleak](https://github.com/hbldh/bleak) powered cross platform python library for controlling [Wonder Workshop's](https://www.makewonder.com/) [Dash](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) robot.

## NOTICE:
Adapted from original source code Copyright 2016 Ilya Sukhanov https://github.com/IlyaSukhanov/morseapi & updated code Copyright 2018 Russ Buchanan https://github.com/havnfun/python-dash-robot

Key differences:
- Changed backend from pygatt to bleak
- Compatible with Python 3.11 
- Cross Platform
- Asynchronous 

## Motivation
I wanted to use my kids dash robot from my Mac or my Windows machine without reinventing the wheel.

## Compatibility
Using Bleak we should be Windows / Mac / Linux agnostic. Please let me know if any issues. Tested on M1 & Windows 
## Getting Started
```
git clone https://github.com/mewmix/bleak-dash
cd bleak-dash
pip install -e . 
```

## Tests

```
python tests/lightshow_random.py  
```

