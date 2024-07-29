import asyncio
from bleak import BleakClient, BleakScanner
from uuid import UUID
import binascii
import logging
import math
import time
from dash.constants import COMMANDS, NOISES, COMMAND1_CHAR_UUID
from dash.sensors import RobotSensors
import struct
from colour import Color
from collections import defaultdict



# Reused the utility functions as they are compatible
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
        self.sense = None
        self.sensor_state = defaultdict(int)

    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        print(f'Connected to {self.address}')

        self.sense = RobotSensors(self.client, self.sensor_state)
        await self.sense.start()

    
    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            logging.info(f"Disconnected from {self.address}")


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

    # Reset method
    async def reset(self, mode=4):
        await self.command("reset", bytearray([mode]))

    # Eye method
    async def eye(self, value):
        await self.command("eye", two_byte_array(value))

    # Eye brightness method
    async def eye_brightness(self, value):
        await self.command("eye_brightness", one_byte_array(value))

    # Neck color method
    async def neck_color(self, color):
        await self.command("neck_color", color_byte_array(color))

    # Left ear color method
    async def left_ear_color(self, color):
        await self.command("left_ear_color", color_byte_array(color))

    # Right ear color method
    async def right_ear_color(self, color):
        await self.command("right_ear_color", color_byte_array(color))

    # Stop method
    async def stop(self):
        await self.command("drive", bytearray([0, 0, 0]))

    async def say(self, sound_name):
        """
        Play a sound from the sound bank file.
        """
        if sound_name in NOISES:
            await self.command("say", bytearray(NOISES[sound_name]))
        else:
            print(f"Sound '{sound_name}' not found in sound bank.")


    # ------------ Sensor Getters for Dot ------------

    def get_time(self) -> float:
        '''
        Returns Dot's/Dash's current Unix time in seconds.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["dot_time"]

    def get_index(self) -> int:
        '''
        Unknown.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["dot_index"]
        
    def get_pitch(self) -> int:
        '''
        Returns Dot's/Dash's current pitch rotation.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["pitch"]
        
    def get_roll(self) -> int:
        '''
        Returns Dot's/Dash's current roll rotation.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["roll"]
        
    def get_acceleration(self) -> int:
        '''
        Returns Dot's/Dash's current acceleration.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["acceleration"]
        
    def is_button_white_pressed(self) -> bool:
        '''
        Returns if Dot's/Dash's white button is being pressed.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["button0"]
        
    def is_button_1_pressed(self) -> bool:
        '''
        Returns if Dot's/Dash's button one is being pressed.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["button1"]
        
    def is_button_2_pressed(self) -> bool:
        '''
        Returns if Dot's/Dash's button two is being pressed.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["button2"]
        
    def is_button_3_pressed(self) -> bool:
        '''
        Returns if Dot's/Dash's button three is being pressed.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["button3"]
        
    def is_moving(self) -> bool:
        '''
        Returns if Dot/Dash is moving.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["moving"]
        
    def is_picked_up(self) -> bool:
        '''
        Returns if Dot/Dash is being picked up.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["picked_up"]
        
    def is_hit(self) -> bool:
        '''
        Returns if Dot/Dash has been hit.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["hit"]
        
    def is_on_side(self) -> bool:
        '''
        Returns if Dot/Dash is laying or tilted on its side.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["side"]
        
    def is_nominal(self) -> bool:
        '''
        Unknown.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["nominal"]
        
    def has_heard_clap(self) -> bool:
        '''
        Returns if Dot/Dash heard a clap in the real world.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["clap"]
        
    def get_mic_level(self) -> int:
        '''
        Returns Dot's/Dash's microphone input level.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["mic_level"]
        
    def is_dot_left_of_dash(self) -> bool:
        '''
        Returns if Dot is to the left of Dash.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["dot_left_of_dash"]
        
    def is_dot_right_of_dash(self) -> bool:
        '''
        Returns if Dot is to the right of Dash.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["dot_right_of_dash"]
        
    def get_robot(self) -> str:
        '''
        Returns which robot type has been connected.
        '''
        if self.sense.dot_data_stream_ready:
            return self.sensor_state["robot"]


class DashRobot(Robot):
    def __init__(self, address):
        super().__init__(address)
        # Additional Dash-specific initialization

    async def tail_brightness(self, value):
        # Ensure the value is within the expected range
        value = max(0, min(255, value))
        await self.command("tail_brightness", one_byte_array(value))

    async def head_yaw(self, angle):
        # Ensure the angle is within the expected range
        angle = max(-53, min(53, angle))
        await self.command("head_yaw", angle_array(angle))

    async def head_pitch(self, angle):
        # Ensure the angle is within the expected range
        angle = max(-5, min(10, angle))
        await self.command("head_pitch", angle_array(angle))
    

    async def drive(self, speed):
        """
        Start moving Dash forward or backward.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x8000 + abs(speed)  # Adjust for negative speeds if necessary
        await self.command("drive", bytearray([
            speed & 0xff,
            (speed >> 8) & 0xff,
            0x00  # Placeholder for potential additional parameters
        ]))

    async def spin(self, speed):
        """
        Start spinning Dash left or right asynchronously.

        Dash will continue spinning until another drive(), spin() or stop()
        command is issued.

        :param speed: Speed at which to spin, 200 is a reasonable value.
        Positive values spin clockwise and negative counter-clockwise.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x8000 + abs(speed)  # Adjust for negative speeds if necessary
        await self.command("drive", bytearray([
            0x00,  # Placeholder for potential additional parameters
            speed & 0xff,
            (speed >> 8) & 0xff
        ]))


        
    async def turn(self, degrees, speed_dps=360/2.094):
        """
        Turns the robot a specific number of degrees at a certain speed.
        This method simplifies the operation to a 'spin' command for a calculated duration.
        Adjust this method based on your robot's capabilities.
        """
        if abs(degrees) > 360:
            print("Cannot turn more than one rotation per move")
            return
        
        # Assuming positive degrees for clockwise, negative for counter-clockwise
        speed = 200 if degrees > 0 else -200
        # Calculate duration based on speed and degrees to turn
        duration = abs(degrees / speed_dps)
        await self.spin(speed)
        await asyncio.sleep(duration)
        await self.stop()
    
    
    async def move(self, distance_mm, speed_mmps=1000, no_turn=True):
        """
        Move specified distance at a particular speed asynchronously.

        :param distance_mm: Distance in mm, negative for backwards.
        :param speed_mmps: Speed in mm/s.
        :param no_turn: Prevents turning if moving backwards when True.
        """
        speed_mmps = abs(speed_mmps)  # Ensure speed is positive
        seconds = abs(distance_mm / speed_mmps)  # Duration of movement
        
        if no_turn and distance_mm < 0:
            byte_array = self._get_move_byte_array(distance_mm, 0, seconds, 0x81)
        else:
            byte_array = self._get_move_byte_array(distance_mm, 0, seconds)
        
        await self.command("move", byte_array)
        logging.debug(f"Moving for {seconds} seconds")
        await asyncio.sleep(seconds)  # Asynchronously wait for movement to complete

    @staticmethod
    def _get_move_byte_array(distance_mm=0, degrees=0, seconds=1.0, eight_byte=0x80):
        """
        Encodes movement parameters into a byte array for BLE command.
        """
        if distance_mm and degrees:
            raise NotImplementedError("Concurrent move and turn not supported.")

        distance_low_byte = distance_mm & 0xFF
        distance_high_byte = (distance_mm >> 8) & 0x3F
        sixth_byte = distance_high_byte
        
        centiradians = int(math.radians(degrees) * 100)
        turn_low_byte = centiradians & 0xFF
        turn_high_byte = (centiradians >> 8) & 0x03
        sixth_byte |= turn_high_byte << 2
        seventh_byte = 0xC0 if centiradians < 0 else 0x00

        time_ms = int(seconds * 1000)
        time_low_byte = time_ms & 0xFF
        time_high_byte = (time_ms >> 8) & 0xFF

        return bytearray([
            distance_low_byte, 0x00, turn_low_byte,
            time_high_byte, time_low_byte, sixth_byte, seventh_byte, eight_byte
        ])
    
    # ------------ Sensor Getters for Dash ------------

    def get_dash_time(self) -> float:
        '''
        Returns Dash's current Unix time in seconds (same as get_time).
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["dash_time"]
        
    def get_dash_index(self) -> int:
        '''
        Unknown. Most times appear as get_index - 1
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["dash_index"]
        
    def get_pitch_delta(self) -> int:
        '''
        Returns the change in pitch, aka delta pitch or Δp, of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["pitch_delta"]
        
    def get_roll_delta(self) -> int:
        '''
        Returns the change in roll, aka delta roll or Δr, of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["roll_delta"]
        
    def get_prox_right(self) -> int:
        '''
        Returns the current distance of an object detected on the right proximity sensor of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["prox_right"]
        
    def get_prox_left(self) -> int:
        '''
        Returns the current distance of an object detected on the left proximity sensor of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["prox_left"]
        
    def get_prox_rear(self) -> int:
        '''
        Returns the current distance of an object detected on the rear proximity sensor of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["prox_rear"]
        
    def get_yaw(self) -> int:
        '''
        Returns Dash's current yaw rotation.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["yaw"]
        
    def get_yaw_delta(self) -> int:
        '''
        Returns the change in yaw, aka delta yaw or Δy, of Dash.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["yaw_delta"]
        
    def get_left_wheel(self) -> int:
        '''
        Returns the current rotation of Dash's left wheel, from 0 - 65535.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["left_wheel"]
        
    def get_right_wheel(self) -> int:
        '''
        Returns the current rotation of Dash's right wheel, from 0 - 65535.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["right_wheel"]
        
    def get_head_pitch(self) -> int:
        '''
        Returns Dash's head's current pitch rotation.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["head_pitch"]
        
    def get_head_yaw(self) -> int:
        '''
        Returns Dash's head's current yaw rotation.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["head_yaw"]
        
    def get_wheel_distance(self) -> int:
        '''
        Returns Dash's current distance traveled.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["wheel_distance"]
        
    def get_sound_direction(self) -> int:
        '''
        Returns the direction of a loud sound detected from Dash's microphone in yaw.
        '''
        if self.sense.dash_data_stream_ready:
            return self.sensor_state["sound_direction"]
        
    


async def discover_and_connect(retry_attempts=3, retry_delay=5):
    attempt = 0
    while attempt < retry_attempts:
        attempt += 1
        logging.info(f"Discovery attempt {attempt} of {retry_attempts}")
        try:
            devices = await BleakScanner.discover()
            for device in devices:
                if device.name == "Dash":
                    logging.info(f"Found Dash at: {device.address}")
                    dash_robot = DashRobot(device.address)
                    await dash_robot.connect()
                    return dash_robot
                elif device.name == "Dot":
                    logging.info(f"Found Dot at: {device.address}")
                    dot_robot = Robot(device.address)
                    await dot_robot.connect()
                    return dot_robot
                elif device.name == "Cue":
                    logging.info(f"Found Cue at: {device.address}")
                    cue_robot = Robot(device.address)
                    await cue_robot.connect()
                    return cue_robot
                
            logging.warning("Compatible device not found. Retrying...")
        except Exception as e:
            logging.error(f"An error occurred during device discovery: {e}")
        await asyncio.sleep(retry_delay)
    logging.error("Failed to discover device after multiple attempts.")
    return None