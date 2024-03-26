from setuptools import setup, find_packages

setup(
    name='bleak-dash',
    version='0.1.0',
    author='Alex Klein',
    author_email='alexanderjamesklein@gmail.com',
    description='An unofficial bleak powered library for controlling Wonder Workshop\'s Dash robot.',
    long_description="""
# bleak-dash

An unofficial [bleak](https://github.com/hbldh/bleak) powered cross-platform Python library for controlling [Wonder Workshop's](https://www.makewonder.com/) [Dash](https://www.makewonder.com/?gclid=CPOO8bC8k8oCFdaRHwodPeMIZg) robot.

## NOTICE
Adapted from original source code Copyright 2016 Ilya Sukhanov (https://github.com/IlyaSukhanov/morseapi) and updated code Copyright 2018 Russ Buchanan (https://github.com/havnfun/python-dash-robot) with key differences:
- Changed backend from pygatt to bleak
- Compatible with Python 3.11
- Cross Platform
- Asynchronous

## Motivation
Designed for use with Dash robot from various operating systems without reinventing the wheel.

## Compatibility
Thanks to Bleak, the library is Windows, Mac, and Linux agnostic. Tested on M1 & Windows.
""",
    long_description_content_type='text/markdown',
    url='https://github.com/mewmix/bleak-dash',
    packages=find_packages(),
    install_requires=[
        'bleak==0.21.1',
        'colour==0.1.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='bleak dash robot wonder workshop asynchronous',
)
