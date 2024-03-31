
import asyncio
import socket

HOST='192.168.232.136' #컴퓨터 시뮬
#HOST='192.168.50.232'  #rap to rap
from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)
#HOST='10.10.88.97'
PORT =65433
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))



async def run():
    """ Does Offboard control using attitude commands. """

    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial:///dev/ttyAMA0")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    #print("Waiting for drone to have a global position estimate...")
    #async for health in drone.telemetry.health():
        #if health.is_global_position_ok and health.is_home_position_ok:
            #print("-- Global position estimate OK")
            #break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    while True:
        #data,addr=sock.recvfrom(1024)
        #my_data=(data.decode().split(":"))
        #roll=(float(my_data[0]))
        #throttle=float(my_data[1])
        #yaw=(float(my_data[2]))
        #pitch=(float(my_data[3])) 
        roll=0
        throttle=0.5
        yaw=0
        pitch=0
        print(roll,throttle,yaw,pitch)
        await drone.offboard.set_attitude(Attitude(yaw, pitch, roll, throttle))
        await asyncio.sleep(0.01)
            
        
    #print("-- Stopping offboard")
    #try:
        #await drone.offboard.stop()
    #except OffboardError as error:
        #print(f"Stopping offboard mode failed with error code: \
              #{error._result.result}")

    #await drone.action.land()


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())