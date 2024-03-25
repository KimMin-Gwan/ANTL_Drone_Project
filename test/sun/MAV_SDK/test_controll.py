from mavsdk import System
import asyncio

async def run():
    drone = System()
    #await drone.connect(system_address="udp://:14540")

    await drone.connect(system_address="serial:///dev/ttyAMA0")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered ")
            break

    await drone.action.arm()
    print("Drone armed")

    await asyncio.sleep(5)  # Let the drone hover for 5 seconds

    # Move the drone forward with a speed of 5 m/s
    await drone.action.set_pitch(0.5)  # Positive value for forward direction
    print("action pithch 0.5")
    await asyncio.sleep(5)  # Let the drone move forward for 5 seconds

    # Stop moving
    await drone.action.set_pitch(0)

    print("action pithch 0")
    await asyncio.sleep(2)  # Pause for 2 seconds

    # Move the drone backward with a speed of 5 m/s
    await drone.action.set_pitch(-0.5)  # Negative value for backward direction

    print("action pithch -0.5")
    await asyncio.sleep(5)  # Let the drone move backward for 5 seconds

    # Stop moving
    await drone.action.set_pitch(0)

    await asyncio.sleep(2)  # Pause for 2 seconds

    # You can similarly control other movements like roll, yaw, and throttle
    # Roll: drone.action.set_roll(value)
    # Yaw: drone.action.set_yaw(value)
    # Throttle: drone.action.set_throttle(value)

    await drone.action.disarm()
    print("Drone disarmed")

asyncio.run(run())
