
import asyncio
from mavsdk import System
class Drone:
    async def __init__(self) -> None:
    #async def make_rone(self):
        self.antl_drone=System()
        await self.antl_drone.connect(system_address="udp://14540")
        
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
            
        print("-- Arming")
        await self.antl_drone.action.arm()
    def get_drone(self):
        return self.antl_drone
class PilotModel:
    def __init__(self):
        self.__key = Key()
        self.__mode = 0

    def set_mode(self, mode):  
        self.__mode = mode
        return

    def set_key(self, key):
        self.__key=key
        return 
    
    def get_key(self):
        return self.__key
    
    def get_mode(self):
        return self.__mode

class Key:
    def __init__(self):
        self.__yaw = 0
        self.__throttle = 0
        self.__pitch = 0
        self.__roll = 0
    ##set
    def set_key(self,yaw,throttle,pitch,roll):
        self.__yaw=yaw
        self.__throttle=throttle
        self.__pitch=pitch
        self.__roll=roll
    ##get
    def get_key(self):
        return (self.__yaw,self.__throttle,self.__pitch,self.__roll)


