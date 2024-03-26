import asyncio
from dash.robot import DashRobot, discover_and_connect

# Function to test Dash-specific movements and interactions
async def test_dash_movements(dash_robot):
    print("Testing Dash-specific movements...")

    # Movement tests
    print("Moving forward slightly...")
    await dash_robot.drive(100)  # Gentle forward movement
    await asyncio.sleep(2)  # Wait for movement to complete

    print("Spinning right...")
    await dash_robot.spin(100)  # Gentle spin right
    await asyncio.sleep(2)

    print("Spinning left...")
    await dash_robot.spin(-100)  # Gentle spin left
    await asyncio.sleep(2)

    print("Moving backward slightly...")
    await dash_robot.drive(-100)  # Gentle backward movement
    await asyncio.sleep(2)

    # Additional Dash capabilities
    print("Adjusting head yaw and pitch...")
    await dash_robot.head_yaw(15)  # Slight turn right
    await asyncio.sleep(1)
    await dash_robot.head_yaw(-15)  # Slight turn left
    await asyncio.sleep(1)
    await dash_robot.head_pitch(5)  # Slight look up
    await asyncio.sleep(1)
    await dash_robot.head_pitch(-5)  # Slight look down
    await asyncio.sleep(1)

    print("Dash-specific movements test completed.")

# Function for basic interactions that both Dot and Dash can perform
async def test_basic_interactions(robot_instance):
    print("Testing basic interactions...")

    # LED and sound interactions
    print("Changing colors...")
    await robot_instance.neck_color("#FF00FF")  # Example color
    await asyncio.sleep(1)
    await robot_instance.left_ear_color("#00FF00")  # Example color
    await asyncio.sleep(1)
    await robot_instance.right_ear_color("#0000FF")  # Example color
    await asyncio.sleep(1)

    print("Playing a sound...")
    await robot_instance.say("hi")  # Play a sound
    await asyncio.sleep(1)

    print("Basic interactions test completed.")

# Main function to discover and test Dash or Dot
async def main():
    robot = await discover_and_connect()
    if not robot:
        print("No compatible robot found.")
        return

    try:
        if isinstance(robot, DashRobot):
            print("Dash detected.")
            await test_dash_movements(robot)
        else:
            print("Dot detected.")

        await test_basic_interactions(robot)

    finally:
        # Ensuring graceful disconnect
        print("Cleaning up and disconnecting...")
        await robot.reset(4)  # Soft reset as a gentle cleanup
        await robot.disconnect()
        print("Disconnected gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
