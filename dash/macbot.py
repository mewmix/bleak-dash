import asyncio
from bleak import BleakClient, BleakScanner, BleakError
import bleak
from uuid import UUID
import binascii
import logging

from dash.constants import HANDLES, COMMANDS, NOISES, COMMAND1_CHAR_UUID
import struct
from colour import Color

# Reuse the utility functions as they are compatible
def one_byte_array(value):
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    color = Color(color_value)
    return bytearray([
        int(round(color.get_red() * 255)),
        int(round(color.get_green() * 255)),
        int(round(color.get_blue() * 255)),
    ])

def angle_array(angle):
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

# Updated robot class using Bleak for BLE operations
class Robot:
    def __init__(self, address):
        self.address = address
        self.client = None

    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        print(f'Connected to {self.address}')

    async def command(self, command_name, command_values):  # Use `self` instead of `client`
            if self.client.is_connected:  # Access `is_connected` through `self.client`
                try:
                    char_uuid = COMMAND1_CHAR_UUID
                    message = bytearray([COMMANDS[command_name]]) + command_values
                    logging.debug(f"Sending command: {binascii.hexlify(message)}")
                    await self.client.write_gatt_char(char_uuid, message)  # Use `self.client` to write
                    logging.info("Command sent successfully.")
                except Exception as e:
                    logging.error(f"Failed to write to characteristic {char_uuid}: {str(e)}")

async def discover_and_connect():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == "Dash":
            print(f"Found Dash at: {device.address}")
            robot = Robot(device.address)
            await robot.connect()
            return robot
    print("Dash not found!")
    return None






# Main program entry point
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    robot = loop.run_until_complete(discover_and_connect())
    # Use robot for further commands...
