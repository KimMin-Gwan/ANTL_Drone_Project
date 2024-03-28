#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")

    # Start the tasks

    asyncio.ensure_future(print_gps_info(drone))

    asyncio.ensure_future(print_position(drone))

    while True:
        await asyncio.sleep(1)



async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")



async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())