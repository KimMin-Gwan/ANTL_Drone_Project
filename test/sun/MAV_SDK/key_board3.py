import asyncio
import keyboard  # 키보드 입력을 처리하는 모듈
from mavsdk import System

# 드론 객체 생성
drone1 = System()
drone2 = System()

# 드론 조종 변수 초기화
roll, pitch, throttle, yaw = 0, 0, 0.5, 0

async def getKeyboardInput(my_drone):
    global roll, pitch, throttle, yaw
    while True:
        # 키보드 입력 처리
        for event in keyboard.read_event():
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'w':
                    throttle = 1
                elif event.name == 's':
                    throttle = 0
                elif event.name == 'a':
                    yaw = -1
                elif event.name == 'd':
                    yaw = 1
                elif event.name == 'up':
                    roll = 1
                elif event.name == 'down':
                    roll = -1
                elif event.name == 'left':
                    pitch = -1
                elif event.name == 'right':
                    pitch = 1
            elif event.event_type == keyboard.KEY_UP:
                if event.name in ['w', 's']:
                    throttle = 0
                elif event.name in ['a', 'd']:
                    yaw = 0
                elif event.name in ['up', 'down']:
                    roll = 0
                elif event.name in ['left', 'right']:
                    pitch = 0

        # 키 입력에 따른 드론 상태 출력
        print(roll, pitch, throttle, yaw)
        await my_drone.manual_control.set_manual_control_input(roll, pitch, throttle, yaw)
        await asyncio.sleep(0.1)

# 드론 연결 및 제어를 위한 비동기 함수
async def run_drone(my_drone, port):
    await my_drone.connect(system_address=f"udp://:145{port}")
    print(f"Waiting for drone {port} to connect...")
    async for state in my_drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone {port}!")
            break
    async for health in my_drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print(f"-- Global position state is good enough for flying for drone {port}.")
            break
    await getKeyboardInput(my_drone)

async def run():
    # 드론을 연결하고 조종하는 비동기 함수 실행
    await asyncio.gather(run_drone(drone1, 40), run_drone(drone2, 41))

if __name__ == "__main__":
    # 메인 비동기 함수 실행
    asyncio.run(run())
