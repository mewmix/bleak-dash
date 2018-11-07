"""
NOTICE:
Adapted from original source code Copyright 2016 Ilya Sukhanov
distributed under Apache 2.0 license
https://github.com/IlyaSukhanov/morseapi
"""

from __future__ import division

from dash.constants import HANDLES, COMMANDS, NOISES
import sys
import uuid
import os
import select
import pygatt
import time
from uuid import UUID

import time
import logging
import struct
import binascii
import math
from collections import defaultdict
from colour import Color

def one_byte_array(value):
    """
    Convert Int to a one byte bytearray

    :param value: value 0-255
    """
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    """
    Convert Int to a two byte bytearray

    :param value: value 0-65535
    """
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    """
    convert color into a 3 byte bytearray

    :param color_value: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
    fully spelled color (e.g. white)
    """
    color = Color(color_value)
    return bytearray([
        int(round(color.get_red()*255)),
        int(round(color.get_green()*255)),
        int(round(color.get_blue()*255)),
    ])

def angle_array(angle):
    """
    Convert angle to a bytearray

    :param angle: Angle -127-127
    """
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

class robot:
    def __init__(self, device):
        print('Returning robot:', device)
        self.device = device
        #print("Connecting to robot Characteristics.")
        #device.discover_characteristics([ROBOT_SERVICE_UUID], [COMMAND1_CHAR_UUID, COMMAND2_CHAR_UUID,  SENSOR1_CHAR_UUID, SENSOR2_CHAR_UUID, INFO_CHAR_UUID])

    def name():
        return self.device.name()

    def command(self, command_name, command_values):
        """
        (from morseapi)
        Send a command to robot

        :param command_name: command name, COMMANDS
        :param command_values: bytearray with command parameters
        """
        message = bytearray([COMMANDS[command_name]]) + command_values
        logging.debug(binascii.hexlify(message))
        if self.device:
            self.device.char_write_handle(HANDLES["command"], message)

    def reset(self, mode=4):
        """
        Reset robot

        ?? not sure about this

        :param mode: Reset
        30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }

        mode

        Available modes:
        1 some kind of debug/reflash mode?
        3 reboot
        4 zero out leds/head
        """
        self.command("reset", bytearray([mode]))

    def eye(self, value):
        """
        Turn on and off the Iris LEDs. There are 12 of them. Top one is the
        first and they are incremeted clockwise.

        Light bottom LED
        >>> bot.eye(1<<6)

        Light alternate LEDs
        >>> bot.eye(0b1010101010101)

        light all LEDs
        >>> bot.eye(8191)

        :param value: bitmask to which light to light up 0-8191
        """
        self.command("eye", two_byte_array(value))

    def eye_brightness(self, value):
        """
        Set brightness of the eye backlight.

        :param value: Brightness value 0-255
        """
        self.command("eye_brightness", one_byte_array(value))

    def neck_color(self, color):
        """
        Set color Neck light on Dash, and Eye backlight on Dot.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.command("neck_color", color_byte_array(color))

    def left_ear_color(self, color):
        """
        Set color of left ear.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.command("left_ear_color", color_byte_array(color))

    def right_ear_color(self, color):
        """
        Set color of right ear.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.command("right_ear_color", color_byte_array(color))

    def ear_color(self, color):
        """
        Set color of both ears.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.left_ear_color(color)
        self.right_ear_color(color)

    def head_color(self, color):
        """
        Set color of top LED.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.command("head_color", color_byte_array(color))

    def say(self, sound_name):
        """
        Play a sound from sound bank file

        :param sound_name: Name of sound to play

        List available noies
        >>> from morseapi import NOISES
        >>> NOISES.keys()
        """
        self.command("say", bytearray(NOISES[sound_name]))

    # All the subsequent commands are Dash specific

    def tail_brightness(self, value):
        """
        Set brightness of the tail backlight.

        :param value: Brightness value 0-255
        """
        self.command("tail_brightness", one_byte_array(value))


    def head_yaw(self, angle):
        """
        Turn Dash's head left or right

        :param angle: distance to turn in degrees from -53 to 53
        """
        angle = max(-53, angle)
        angle = min(53, angle)
        self.command("head_yaw", angle_array(angle))

    def head_pitch(self, angle):
        """
        Tilt Dash's head up or down.

        :param angle: distance to turn from -5 to 10
        """
        angle = max(-5, angle)
        angle = min(10, angle)
        self.command("head_pitch", angle_array(angle))

    def stop(self):
        """
        Stop moving Dash.
        """
        self.command("drive", bytearray([0, 0, 0]))

    def drive(self, speed):
        """
        Start moving Dash forward or backward.

        Dash will continue moving until another drive(), spin() or stop()
        command is issued.

        :param speed: Speed at which to move, 200 is a resonable value.
        Negative speed drives Dash backwards.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        self.command("drive", bytearray([
            speed & 0xff,
            0x00,
            (speed & 0x0f00) >> 8
        ]))

    def spin(self, speed):
        """
        Start spinning Dash left or right.

        Dash will continue spinning until another drive(), spin() or stop()
        command is issued.

        :param speed: Speed at which to spin, 200 is a reasonable value.
        Positive values spin clockwise and negative counter-clockwise.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        self.command("drive", bytearray([
            0x00,
            speed & 0xff,
            (speed & 0xff00) >> 5
        ]))

    def turn(self, degrees, speed_dps=(360/2.094)):
        """
        Turn Dash specified distance.

        This is a blocking call.

        :param degrees: How many degrees to turn.
        Positive values spin clockwise and negative counter-clockwise.
        :param speed: Speed to turn at, in degrees/second
        """
        if abs(degrees) > 360:
            raise NotImplementedError("Cannot turn more than one rotation per move")
        if degrees:
            seconds = abs(degrees/speed_dps)
            byte_array = self._get_move_byte_array(degrees=degrees, seconds=seconds)
            self.command("move", byte_array)
            logging.debug("turn sleeping {0} @ {1}".format(seconds, time.time()))
            logging.debug(binascii.hexlify(byte_array))
            # self.sleep does not work and api says not to use time.sleep...
            time.sleep(seconds)
            logging.debug("turn finished sleeping {0} @ {1}".format(seconds, time.time()))

    def move(self, distance_mm, speed_mmps=1000, no_turn=True):
        """
        Move specified distance at a particular speed.

        This is a blocking call.

        :param distance_mm: How far to move in mm. Negative values to go backwards
        :param speed_mmps: Speed at which to move in mm/s.
        """
        speed_mmps = abs(speed_mmps)
        seconds = abs(distance_mm / speed_mmps)
        if no_turn and distance_mm < 0:
            byte_array = self._get_move_byte_array(
                distance_mm=distance_mm,
                seconds=seconds,
                eight_byte=0x81,
            )
        else:
            byte_array = self._get_move_byte_array(
                distance_mm=distance_mm,
                seconds=seconds,
            )
        self.command("move", byte_array)
        logging.debug("move sleeping {0} @ {1}".format(seconds, time.time()))
        logging.debug(binascii.hexlify(byte_array))
        # self.sleep does not work and api says not to use time.sleep...
        time.sleep(seconds)
        logging.debug("move finished sleeping {0} @ {1}".format(seconds, time.time()))

    @staticmethod
    def _get_move_byte_array(distance_mm=0, degrees=0, seconds=1.0, eight_byte=0x80):
        # Sixth byte is mixed use
        # * turning
        #   * high nibble is turn distance high byte<<2
        #   * low nibble is 0
        # * driving straight
        #   * whole byte is high byte of drive distance
        # unclear if these can be combined
        # Eight byte is weird.
        # * On subsequent move commands its usually 0x40
        # * On first command its usually 0x80, but not required
        # * When driving backwards without turning around last bit is 1
        if distance_mm and degrees:
            raise NotImplementedError("Cannot turn and move concurrently")

        sixth_byte = 0
        seventh_byte = 0

        distance_low_byte = distance_mm & 0x00ff
        distance_high_byte = (distance_mm & 0x3f00) >> 8
        sixth_byte |= distance_high_byte

        centiradians = int(math.radians(degrees) * 100.0)
        turn_low_byte = centiradians & 0x00ff
        turn_high_byte = (centiradians & 0x0300) >> 2
        sixth_byte |= turn_high_byte
        if centiradians < 0:
            seventh_byte = 0xc0

        time_measure = int(seconds * 1000.0)
        time_low_byte = time_measure & 0x00ff
        time_high_byte = (time_measure & 0xff00) >> 8

        return bytearray([
            distance_low_byte,
            0x00,  # unknown
            turn_low_byte,
            time_high_byte,
            time_low_byte,
            sixth_byte,
            seventh_byte,
            eight_byte,
        ])

def get_dash():
    adapter = pygatt.GATTToolBackend()
    address = ''

    adapter.start()
    devices = adapter.scan(run_as_root=True, timeout=3)
    for device in devices:
        if device['name'] == 'Dash':
            address = device['address']
            print('Found Dash at:', address)

    if address != '':
        print('Connecting to:', address)
        x = adapter.connect(address, address_type=pygatt.BLEAddressType.random)
        dash = robot(x)
    else:
        print('Dash not found!')
        dash = None

    return dash
