
import asyncio
from mavsdk import System, OffboardError, Attitude


class ANTL_DRONE:
    def __init__(self):
        self.drone = System()

    async def connect(self):
        await self.drone.connect(system_address="udp://:14540")

    async def wait_for_connection(self):
        print("Waiting for drone to connect...")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("-- Connected to drone!")
                break

    async def wait_for_global_position_estimate(self):
        print("Waiting for drone to have a global position estimate...")
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position estimate OK")
                break

    async def arm_drone(self):
        print("-- Arming")
        await self.drone.action.arm()

    async def set_initial_setpoint(self):
        print("-- Setting initial setpoint")
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))
    async def start_offboard_mode(self):
        print("-- Starting offboard")
        try:
            await self.drone.offboard.start()
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: \
                  {error._result.result}")
            print("-- Disarming")
            await self.drone.action.disarm()
            return
    async def go_up(self):
        print("-- Go up at 70% thrust")
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.7))
        await asyncio.sleep(3)
        
    async def stop_offboard_mode(self):
        print("-- Stopping offboard")
        try:
            await self.drone.offboard.stop()
        except OffboardError as error:
            print(f"Stopping offboard mode failed with error code: \
                  {error._result.result}")

    async def land_drone(self):
        await self.drone.action.land()

    async def run(self):
        await self.connect()
        await self.wait_for_connection()
        await self.wait_for_global_position_estimate()
        await self.arm_drone()
        await self.set_initial_setpoint()
        await self.start_offboard_mode()
        while True:
            a,b,c,d=int(input(input("input y1,x1,y2,x,2")))
            if(a==-1):
                break
            a, b, c, d = map(int, input("스로틀 , YAW , PITCH , ROLL ").split())
            await self.get_stick_value(a,b,c,d) 
            
        await self.stop_offboard_mode()
    async def get_stick_value(self,throtle, yaw, pitch,roll):
        #0~100 throtle 은 0.0~1.0 사이로 넣는 느낌으로 
        await self.drone.offboard.set_attitude(Attitude(pitch, yaw, roll, throtle))
        await asyncio.sleep(0.1)
        
# 실행 예제
if __name__ == "__main__":
    antl_drone = ANTL_DRONE()
    asyncio.run(antl_drone.run())
