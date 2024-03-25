import asyncio
from mavsdk import System


async def manual_control():
    # Connect to the MAVLink system
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered.")
            break

    # Start manual control
    await drone.manual_control.start_position_control()

    # Control loop
    try:
        while True:
            # Read user input
            command = input("Enter command (WASDQE): ").lower()

            # Process user input
            if command == "w":
                await drone.manual_control.set_velocity_ned(0.0, 1.0, 0.0, 0.0)
            elif command == "s":
                await drone.manual_control.set_velocity_ned(0.0, -1.0, 0.0, 0.0)
            elif command == "a":
                await drone.manual_control.set_velocity_ned(-1.0, 0.0, 0.0, 0.0)
            elif command == "d":
                await drone.manual_control.set_velocity_ned(1.0, 0.0, 0.0, 0.0)
            elif command == "q":
                await drone.manual_control.set_velocity_ned(0.0, 0.0, -1.0, 0.0)
            elif command == "e":
                await drone.manual_control.set_velocity_ned(0.0, 0.0, 1.0, 0.0)
            elif command == "stop":
                break
            else:
                print("Invalid command. Use WASDQE keys.")

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected.")

    finally:
        # Stop manual control and disconnect
        await drone.manual_control.stop()
        await drone.disconnect()


if __name__ == "__main__":
    asyncio.run(manual_control())
