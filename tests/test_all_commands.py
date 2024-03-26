import asyncio
from dash.robot import Robot, discover_and_connect
from dash.constants import COMMANDS

async def test_all_commands():
    robot = await discover_and_connect()
    if robot:
        print("Robot connected. Testing all commands...")
        for command_name, command_code in COMMANDS.items():
            # Prepare message for the command
            message = bytearray([command_code])
            await robot.command(command_name, message)
            print(f"Command '{command_name}' sent.")
            
            await asyncio.sleep(2)  
            
        print("Stopping robot...")
        await robot.stop()
        print("Robot stopped.")
    else:
        print("Failed to connect to the robot.")

if __name__ == "__main__":
    asyncio.run(test_all_commands())
