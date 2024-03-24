import asyncio
from dash.macbot import Robot, discover_and_connect
from dash.constants import COMMANDS

async def test_all_commands():
    robot = await discover_and_connect()
    if robot:
        print("Robot connected. Testing all commands...")
        for command_name, command_code in COMMANDS.items():
            # Prepare message for the command (assuming no additional parameters are needed)
            message = bytearray([command_code])
            await robot.command(command_name, message)
            print(f"Command '{command_name}' sent.")
    else:
        print("Failed to connect to the robot.")

if __name__ == "__main__":
    asyncio.run(test_all_commands())
