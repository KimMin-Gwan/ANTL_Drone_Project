import asyncio
import random
import socket
from mavsdk import System
from information.constant import *
class Drone():
    def __init__(self,interface) -> None:
        self.antl_drone=None
        self.interface=interface 
    async def make_drone(self):
        
        self.antl_drone=System()
        
        await self.antl_drone.connect(system_address=VMWARE_SYSTEM_ADDRESS)
        
        print("Wating for drone to connect...")  #drone connect 
        async for state in self.antl_drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break
        # Checking if Global Position Estimate is ok
        async for health in self.antl_drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position state is good enough for flying.")
                break
            
        
        await self.arming()
        self.interface.set_drone_flag(1) 
        print("==================완료")
        
        
    async def arming(self):
        print("-- Arming")
        await self.antl_drone.action.arm()
    
    async def TakingOff(self):
        print("-- Taking off")
        await self.antl_drone.action.takeoff()
        await asyncio.sleep(2)
    
    
    def get_drone(self):
        return self.antl_drone