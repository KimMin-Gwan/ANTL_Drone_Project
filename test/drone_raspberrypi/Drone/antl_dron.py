import asyncio
import random
import socket
from mavsdk import System
from Information.constant import *

class drone():
    async def __init__(self) -> None:
        self.drone=System()
        
        await self.drone.connect(system_address=VMWARE_SYSTEM_ADDRESS)
        
        print("Wating for drone to connect...")  #drone connect 
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break
        # Checking if Global Position Estimate is ok
        async for health in drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position state is good enough for flying.")
                break
    async def arming(self):
        print("-- Arming")
        await self.drone.arm()
    
    async def TakingOff(self):
        print("-- Taking off")
        await drone.action.takeoff()
        await asyncio.sleep(2)
    
    def get_drone(self):
        return self.drone