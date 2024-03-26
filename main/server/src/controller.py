from model import VideoModel
from model import PilotModel
import cv2

class VideoController:
    def __init__(self):
        self.__video_model = VideoModel()

    # 드론으로 부터 비디오 받는부분
    def recv_video(self, frame):
        pass

    # 비디오를 사용자에게 보내는 부분
    def get_frame(self):
        while True:
            try:
                frame = self.__video_model.get_frame()
                if frame:
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                # 가짜 임시 데이터
                else:
                    frame = self.__video_model.get_default_frame()
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
            except:
                frame = self.__video_model.get_default_frame()
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
            finally:
                yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                

class PilotController():
    def __init__(self):
        self.__pilot_model = PilotModel()


                
