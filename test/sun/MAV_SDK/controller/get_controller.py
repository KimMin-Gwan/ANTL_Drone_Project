import asyncio
from mavsdk import System

async def print_rc_input():
    # 시스템에 연결
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")
    print("connected!!!")
    # RC 입력 구독 시작
    async for rc_input in drone.telemetry.rc_status():
        print("Throttle:", rc_input.values.throttle)
        print("Roll:", rc_input.values.roll)
        print("Pitch:", rc_input.values.pitch)
        print("Yaw:", rc_input.values.yaw)

# asyncio 루프 시작
async def main():
    await print_rc_input()

if __name__ == "__main__":
    asyncio.run(main())
