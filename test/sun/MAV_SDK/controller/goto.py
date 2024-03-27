#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)



async def run():
    """ Does Offboard control using velocity NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go up 2 m/s")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, -2.0, 0.0))
    await asyncio.sleep(4)

        
    while True:
            (throtle, yaw, pitch, roll) = map(float, input("스로틀 , YAW , PITCH , ROLL ").split())
            if(a==-1):
                break
            print("your input is ")
            print(a,b,c,d)
            print("조종 들어갑니다.")
            await self.drone.offboard.set_attitude(Attitude(pitch, yaw, roll, throtle))
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
              {error._result.result}")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())