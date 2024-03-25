#!/usr/bin/env python3

import asyncio
import sys
import termios
import tty

from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError


async def get_keypress():
    """Non-blocking function to get a single keypress."""
    # Save old terminal settings
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        # Get a single character
        key = sys.stdin.read(1)
        return key
    finally:
        # Restore old terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


async def main():
    # Connect to the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    # Initial setpoint
    current_setpoint = PositionNedYaw(0.0, 0.0, 0.0, 0.0)

    # Offboard mode
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("Use arrow keys to move the drone. Press 'q' to quit.")

    while True:
        key = await get_keypress()

        if key == '\x1b[A':  # Up arrow key
            current_setpoint = PositionNedYaw(current_setpoint.north_m + 1, current_setpoint.east_m,
                                              current_setpoint.down_m, current_setpoint.yaw_deg)
        elif key == '\x1b[B':  # Down arrow key
            current_setpoint = PositionNedYaw(current_setpoint.north_m - 1, current_setpoint.east_m,
                                              current_setpoint.down_m, current_setpoint.yaw_deg)
        elif key == '\x1b[C':  # Right arrow key
            current_setpoint = PositionNedYaw(current_setpoint.north_m, current_setpoint.east_m + 1,
                                              current_setpoint.down_m, current_setpoint.yaw_deg)
        elif key == '\x1b[D':  # Left arrow key
            current_setpoint = PositionNedYaw(current_setpoint.north_m, current_setpoint.east_m - 1,
                                              current_setpoint.down_m, current_setpoint.yaw_deg)
        elif key == 'q':  # Quit
            break

        # Update setpoint
        await drone.offboard.set_position_ned(current_setpoint)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Disarming")
    await drone.action.disarm()


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())
