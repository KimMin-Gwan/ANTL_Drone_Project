from main.server.src.model.model import VideoModel
from main.server.src.model.model import PilotModel
import cv2



# 이 인스턴스도 한번 생성되면 사라지지 않아야함
class VideoController:
    def __init__(self):
        self.__video_model = VideoModel()

    # 드론으로 부터 비디오 받는부분
    def recv_video(self, frame):
        colored_frame= cv2.imencode(frame, cv2.IMREAD_COLOR)
        self.__video_model.set_frame(frame=colored_frame)
        return

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
                
# 이 인스턴스는 한번 생성되면 사라지지 않아야함
class PilotController():
    def __init__(self):
        self.__pilot_model = PilotModel()

    # 들어온 값 그대로 유지하면 될듯
    #data = "key x1 y1 x2 y2"
    #data = "mode 0"
    def try_recv_control(self, data:str):
        s_data = data.split(" ")
        header = s_data[0]
        if header == "key":
            keys = s_data[1:5]
            self.__set_control_key(self, keys=keys)
        elif header == "mode":
            mode = s_data[1]
            self.__set_mode(self, mode=mode)
        else:
            # 예외처리 필요
            return
        return

    # key 값 보내기
    def try_send_control(self):
        keys:tuple = self.__pilot_model.get_key()
        return keys

    # key 값 설정하기
    def __set_control_key(self, keys:list):
        n_keys = []
        for k in keys:
            n_key = int(k)
            n_keys.append(n_key)

        self.__pilot_model.set_key(
            x1=n_keys[0], y1=n_keys[1],
            x2=n_keys[2], y2=n_keys[3])
        return

    # mode 변경하기
    def __set_mode(self, mode):
        n_mode:int = int(mode)
        self.__pilot_model.set_mode(mode=n_mode)
        return



                
