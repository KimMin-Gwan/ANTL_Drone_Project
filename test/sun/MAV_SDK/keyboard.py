import asyncio
from mavsdk import System
import keyboard  # Import the keyboard module

# Initialize drone
drone = System()

# Initialize manual control inputs
roll, pitch, throttle, yaw = 0, 0, 0.5, 0

async def getKeyboardInput():
    """
    Get manual keyboard inputs for controlling the drone.
    """
    global roll, pitch, throttle, yaw
    while True:
        # Reset manual control inputs
        roll, pitch, throttle, yaw = 0, 0, 0.5, 0

        # Check keyboard inputs
        value = 1
        if keyboard.is_pressed("LEFT"):
            pitch = -value
        elif keyboard.is_pressed("RIGHT"):
            pitch = value
        if keyboard.is_pressed("UP"):
            roll = value
        elif keyboard.is_pressed("DOWN"):
            roll = -value
        if keyboard.is_pressed("w"):
            throttle = value
        elif keyboard.is_pressed("s"):
            throttle = 0
        if keyboard.is_pressed("a"):
            yaw = -value
        elif keyboard.is_pressed("d"):
            yaw = value
        elif keyboard.is_pressed("i"):
            asyncio.ensure_future(print_flight_mode())
        elif keyboard.is_pressed("q") and drone.telemetry.landed_state():
            await drone.action.arm()
        elif keyboard.is_pressed("l") and drone.telemetry.in_air():
            await drone.action.land()
        await asyncio.sleep(0.1)

async def print_flight_mode():
    """
    Print the flight mode of the drone.
    """
    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)

async def manual_control_drone():
    """
    Manually control the drone based on keyboard inputs.
    """
    global roll, pitch, throttle, yaw
    while True:
        print(roll, pitch, throttle, yaw)
        await drone.manual_control.set_manual_control_input(roll, pitch, throttle, yaw)
        await asyncio.sleep(0.1)

async def run():
    """
    Main function to connect to the drone and input manual controls.
    """
    await drone.connect(system_address="serial:///dev/ttyAMA0")
    # This waits until a mavlink-based drone is connected
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    # Checking if Global Position Estimate is ok
    # async for health in drone.telemetry.health():
    #     if health.is_global_position_ok and health.is_home_position_ok:
    #         print("-- Global position state is good enough for flying.")
    #         break
    # Run keyboard input and manual control tasks concurrently
    await asyncio.gather(getKeyboardInput(), manual_control_drone())

if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Run the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()

