import asyncio
from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)
async def connect_to_drone():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    return drone

async def get_user_input():
    print("속도와 yaw 회전 속도를 입력하세요.")
    print("포맷: <북쪽 방향 속도> <동쪽 방향 속도> <아래쪽 방향 속도> <yaw 회전 속도>")
    print("예시: 1.0 0.0 0.0 0.5 (북쪽으로 1m/s, yaw 회전 속도는 0.5 rad/s)")

    while True:
        try:
            user_input = input("입력: ")
            values = [float(val) for val in user_input.split()]
            if len(values) != 4:
                raise ValueError("입력 값이 올바르지 않습니다.")
            return values
        except ValueError as e:
            print(f"에러: {e}")

async def control_drone(drone):
    await drone.offboard.set_velocity_ned_yaw(0.0, 0.0, 0.0, 0.0)
    print("드론 제어를 시작합니다.")

    while True:
        user_values = await get_user_input()
        try:
            await drone.offboard.set_velocity_ned_yaw_noreturn(*user_values)
        except OffboardError as error:
            print(f"Offboard 제어 오류: {error}")
            return

async def main():
    drone = await connect_to_drone()

    await control_drone(drone)

if __name__ == "__main__":
    asyncio.run(main())
