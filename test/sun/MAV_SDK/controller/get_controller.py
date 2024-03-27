


import asyncio
from mavsdk import System

async def connect_to_drone():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")  # Pixhawk 4와의 UART 연결
    print("connected!!!!")
    return drone

async def get_rc_values(drone):
    async for rc_data in drone.telemetry.rc_status():
        rc_channels = rc_data.rc_channels
        yaw = rc_channels[0]
        pitch = rc_channels[1]
        roll = rc_channels[2]
        throttle = rc_channels[3]
        print("Yaw:", yaw, "Pitch:", pitch, "Roll:", roll, "Throttle:", throttle)
        
async def main():
    drone = await connect_to_drone()
    await asyncio.gather(
        get_rc_values(drone),
        # 여기에 다른 작업을 추가할 수 있음
    )

if __name__ == "__main__":
    asyncio.run(main())
