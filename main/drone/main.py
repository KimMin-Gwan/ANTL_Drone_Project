from src.view import RealTimeAPI
from src.controller import MasterController
from threading import Thread
from src.constants import HOST, PORT

def main():
    master = MasterController()
    app = RealTimeAPI()
    video_thread = Thread(target=master.get_video_frame)
    video_thread.start()
    app.try_connect(controller=master, host=HOST, port=PORT)


if __name__ == "__main__":
    main()