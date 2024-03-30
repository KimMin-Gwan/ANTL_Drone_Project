
from controller.pilot_controller import PilotController
from controller.video_controller import VideoController
from controller.object_controller import ObjectController
from model import VideoModel
from model import ModeModel
from threading import Thread

class MasterController:
    def __init__(self):
        self.__pilot_controller = None
        self.__video_model = VideoModel()
        self.__mode = ModeModel()
        self.__video_controller = VideoController(video_model=self.__video_model)
        self.__object_controller = ObjectController(self.__video_model, self.__mode)


    async def run(self):
        self.__video_controller.run_camera()
        self.__object_controller.run_object_detector()
        await self.__run_pilot()

    async def __run_pilot(self):
        try:
            self.__pilot_controller = PilotController(mode=self.__mode)
            await self.__pilot_controller.init_drone()
            await self.__pilot_controller.run()
        except:
            print("Asyncio did Bad action")

    def get_video(self):
        frame = self.__video_model.get_raw_frame()
        return frame

    def set_recv_data(self, key_data, mode_data):
        key = [0, 0, 0, 0]
        mode = int(mode_data)
        # mode : 0 -> manual, 1 -> auto
        if self.__mode.get_mode() != mode:
            self.__mode.set_mode(mode)
            self.__video_controller.swap_camera()
        
        # 자동 조작 모드
        if mode:
            try:
                key = self.__object_controller.get_key()
            except:
                key = [0, 0.3, 0, 0]
        else: # 수동 조작모드
            key.clear()
            for k in key_data:
                key.append(float(k))
        try:
            self.__pilot_controller.set_key(key=key)
        except:
            print("ERROR :: pilot _controller did not maked")
        return


        



