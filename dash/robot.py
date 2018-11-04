from __future__ import division

from . import constants
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

# our dash
# ADDRESS = 'DA:40:EB:1A:1C:07'
# ADDRESS_TYPE = pygatt.BLEAddressType.random

# Sounds
HI = '1853595354444153485f48495f564f'
HUH = '1853595354435552494f55535f3034'
UHOH = '1853595354574855485f4f485f3230'
OKAY = '1853595354424f5f4f4b41595f3033'
SIGH = '1853595354424f5f56375f5941574e'
TADA = '18535953545441485f4441485f3031'
WEE = '1853595354455843495445445f3031'
BYE = '1853595354424f5f56375f56415249'
HORSE = '1853595354484f5253455748494e32'
CAT = '185359535446585f4341545f303100'
DOG = '185359535446585f444f475f303200'
DINOSAUR = '185359535444494e4f534155525f33'
LION = '185359535446585f4c494f4e5f3031'
GOAT = '185359535446585f30335f474f4154'
CROCODILE = '185359535443524f434f44494c4500'
ELEPHANT = '1853595354454c455048414e545f30'
FIRESIREN = '1853595354585f534952454e5f3032'
TRUCKHORN = '1853595354545255434b484f524e00'
CARENGINE = '1853595354454e47494e455f524556'
CARTIRESQUEEL = '18535953545449524553515545414c'
HELICOPTER = '185359535448454c49434f50544552'
JETPLANE = '1853595354414952504f52544a4554'
BOAT = '1853595354545547424f41545f3031'
TRAIN = '1853595354545241494e5f57484953'
BEEPS = '1853595354424f545f435554455f30'
LASERS = '18535953544f545f435554455f3033'
GOBBLE = '1853595354474f42424c455f303031'
BUZZ = '185359535455535f4c495042555a5a'
AYYAIYAI = '1853595354434f4e46555345445f31'
SQUEEK = '18535953544f545f435554455f3034'
MYSOUND1 = '1853595354564f4943453000000000'
MYSOUND2 = '1853595354564f4943453100000000'
MYSOUND3 = '1853595354564f4943453200000000'
MYSOUND4 = '1853595354564f4943453300000000'
MYSOUND5 = '1853595354564f4943453400000000'
MYSOUND6 = '1853595354564f4943453500000000'
MYSOUND7 = '1853595354564f4943453600000000'
MYSOUND8 = '1853595354564f4943453700000000'
MYSOUND9 = '1853595354564f4943453800000000'
MYSOUND10 = '1853595354564f4943453900000000'



# uhoh SYSTWHUH_OH_20'
# okay SYSTBO_OKAY_03'
# yawn SYSTBO_V7_YAWN'
# tada SYSTTAH_DAH_01'
# wee SYSTEXCITED_01'
# bye SYSTBO_V7_VARI'
# horse SYSTHORSEWHIN2'
# cat SYSTFX_CAT_01\x00'
# dog SYSTFX_DOG_02\x00'
# dino SYSTDINOSAUR_3'
# lion SYSTFX_LION_01'
# goat 8SYSTFX_03_GOAT'
# croc SYSTCROCODILE\x00'
# siren SYSTX_SIREN_02'
# horn SYSTTRUCKHORN\x00'
# rev SYSTENGINE_REV'
# engine SYSTTIRESQUEAL'
# helicopter SYSTHELICOPTER'
# jet SYSTAIRPORTJET'
# boat SYSTTUGBOAT_01'
# train SYSTTRAIN_WHIS'
# beep SYSTBOT_CUTE_0'
# buzz SYSTUS_LIPBUZZ'
# squeek SYSTOT_CUTE_04'
# my1 SYSTVOICE0\x00\x00\x00\x00'
# my2 SYSTVOICE1\x00\x00\x00\x00'
# my3 SYSTVOICE2\x00\x00\x00\x00'
# my4 SYSTVOICE3\x00\x00\x00\x00'
# my5 SYSTVOICE4\x00\x00\x00\x00'
# my6 SYSTVOICE5\x00\x00\x00\x00'
# my7 SYSTVOICE6\x00\x00\x00\x00'
# my8 SYSTVOICE7\x00\x00\x00\x00'
# my9 SYSTVOICE8\x00\x00\x00\x00'
# my10 SYSTVOICE9\x00\x00\x00\x00'


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
        print('Connecting to:', device)
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
        dash = adapter.connect(address, address_type=pygatt.BLEAddressType.random)
    else:
        print('Dash not found!')
        dash = None

    return dash



#dash = adapter.connect(address, address_type=ADDRESS_TYPE)
