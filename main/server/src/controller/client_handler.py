from main.server.src.controller.controller import VideoController, PilotController


class ClientController:
    def __init__(self):
        self.__vc = VideoController()
        self.__pc = PilotController()

    def get_video_controller(self):
        return self.__vc

    def get_pilot_controller(self):
        return self.__pc