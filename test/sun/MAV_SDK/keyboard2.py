import asyncio
import sys
import termios
import tty
from mavsdk import System
from mavsdk.offboard import OffboardError
from mavsdk import OffboardVelocityNedYaw


async def manual_control():
    # Connect to the MAVLink system
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered.")
            break

    # Start offboard control
    try:
        await drone.offboard.start()

        # Control loop
        while True:
            # Read user input
            command = getch()

            # Process user input
            if command == "w":
                await send_velocity_command(drone, 2.0, 0.0, 0.0, 0.0)
            elif command == "s":
                await send_velocity_command(drone, -2.0, 0.0, 0.0, 0.0)
            elif command == "a":
                await send_velocity_command(drone, 0.0, -2.0, 0.0, 0.0)
            elif command == "d":
                await send_velocity_command(drone, 0.0, 2.0, 0.0, 0.0)
            elif command == "q":
                await send_velocity_command(drone, 0.0, 0.0, -1.0, 0.0)
            elif command == "e":
                await send_velocity_command(drone, 0.0, 0.0, 1.0, 0.0)
            elif command == "stop":
                break
            else:
                print("Invalid command. Use WASDQE keys.")

    except OffboardError as error:
        print(f"Offboard control failed with error code: {error._result}")

    finally:
        # Stop offboard control and disconnect
        await drone.offboard.stop()
        await drone.disconnect()


async def send_velocity_command(drone, velocity_x, velocity_y, velocity_z, yaw):
    offboard_velocity_ned_yaw = OffboardVelocityNedYaw()
    offboard_velocity_ned_yaw.velocity_north_m_s = velocity_x
    offboard_velocity_ned_yaw.velocity_east_m_s = velocity_y
    offboard_velocity_ned_yaw.velocity_down_m_s = velocity_z
    offboard_velocity_ned_yaw.yaw_deg = yaw
    await drone.offboard.set_velocity_ned_yaw(offboard_velocity_ned_yaw)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == "__main__":
    asyncio.run(manual_control())
