import asyncio
from dash.robot import DashRobot, discover_and_connect
import logging
import random

async def run_light_show(robot):
    # Define a list of rave colors for the light show
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF', '#FFA500', '#FF1493', '#8A2BE2', '#00CED1', '#32CD32', '#FFD700', '#FF4500']
    
    # Run the rave light show
    logging.info("Starting rave light show...")
    for _ in range(50):  # Run the show for 50 cycles
        # Generate random colors for each light
        neck_color = random.choice(colors)
        ear_color = random.choice(colors)
        eye_pattern = random.randint(1, 4095)  # Random pattern for eye LEDs
        tail_brightness = random.randint(150, 255)  # Random brightness for tail light
        
        # Set random colors and patterns for each light
        if hasattr(robot, 'neck_color'):
            await robot.neck_color(neck_color)
        if hasattr(robot, 'left_ear_color') and hasattr(robot, 'right_ear_color'):
            await robot.left_ear_color(ear_color)
            await robot.right_ear_color(ear_color)
        if hasattr(robot, 'eye'):
            await robot.eye(eye_pattern)
        if hasattr(robot, 'tail_brightness'):
            await robot.tail_brightness(tail_brightness)
        
        # Delay to create a strobe effect
        await asyncio.sleep(0.2)  # Short delay for fast strobe effect
    
    # Turn off all lights at the end
    if hasattr(robot, 'neck_color'):
        await robot.neck_color('#000000')  # Turn off neck light
    if hasattr(robot, 'left_ear_color') and hasattr(robot, 'right_ear_color'):
        await robot.left_ear_color('#000000')  # Turn off left ear light
        await robot.right_ear_color('#000000')  # Turn off right ear light
    if hasattr(robot, 'eye'):
        await robot.eye(0)  # Turn off eye LEDs
    if hasattr(robot, 'tail_brightness'):
        await robot.tail_brightness(0)  # Turn off tail light
    
    logging.info("Rave light show completed.")

async def main():
    logging.basicConfig(level=logging.INFO)
    robot = await discover_and_connect()
    if robot is not None:
        await run_light_show(robot)
        await robot.disconnect()
    else:
        logging.error("Failed to connect to a robot.")

if __name__ == "__main__":
    asyncio.run(main())
