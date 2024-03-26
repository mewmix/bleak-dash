import asyncio
from dash.robot import DashRobot, discover_and_connect

async def test_move(robot):
    print("Testing move functionality...")
    # Move forward a small distance at a moderate speed
    await robot.move(100, 100)  # Move 100mm at 100mm/s
    print("Move test completed.")

async def main():
    robot = await discover_and_connect()
    if not robot:
        print("No compatible robot found.")
        return

    if isinstance(robot, DashRobot):
        print("Dash detected. Proceeding with move test.")
        await test_move(robot)
    else:
        print("Robot detected is not a Dash. Move test is specific to Dash.")

    # Ensure graceful disconnect regardless of test outcome
    print("Cleaning up and disconnecting...")
    await robot.disconnect()
    print("Disconnected gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
