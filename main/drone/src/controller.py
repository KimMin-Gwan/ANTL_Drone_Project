## 드론 조작에 관한 모든 구현
#from model import VideoModel
from model import PilotModel, VideoModel
from constants import WAIT_IMG_PATH
import cv2

class MasterController():
    def __init__(self):
        self.__key_controller = KeyController()
        self.__video_controller = VideoController()

    def get_video_frame(self):
        return self.__video_controller.get_frame()

    def set_control_key(self, keys):
        return self.__key_controller.set_control_key(keys)

    def run_video_capture(self):
        while True:
            try:
                self.__video_controller.set_frame()
            except:
                print(">> Caputure Error")
                continue

class VideoController():
    def __init__(self):
        self.__video_model = VideoModel()

    def get_frame(self):
        return self.__video_model.get_frame()

    def set_frame(self):
        ret, frame = self.__video_model.get_cap().read()
        if not ret:
            frame = cv2.imread(WAIT_IMG_PATH)
        self.__video_model.set_raw_frame(frame)
        frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY], 90)
        self.__video_model.set_frame(frame)
        return


# 임시 데이
class KeyController():
    def __init__(self):
        self.__pilot_Model = PilotModel()

    # data size : 0 <  x < 1000
    def set_control_key(self, keys):
        n_keys = []
        for k in keys:
            n_key = int(k)
            key:float = n_key * 0.001
            n_keys.append(key)
        self.__pilot_Model.set_key(n_keys)

