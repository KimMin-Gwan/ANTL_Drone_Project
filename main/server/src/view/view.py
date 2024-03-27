from fastapi import FastAPI
from main.server.src.view.real_time_api import RealTimeAPI
import uvicorn
from main.server.src.view.constants import HOST, PORT, RT_PORT_APK, RT_PORT_DR
from main.server.src.view.real_time_api import mingcorn
import threading
from threading import Thread
from fastapi.responses import StreamingResponse
from main.server.src.controller.controller import VideoController
from main.server.src.controller.client_handler import ClientController
from main.server.src.view.data_parser import Parser

# APP
# ASGI 를 활성화하려면 매게변수로 client를 받아보든가
class APP_View():
    def __init__(self):
        self.rt_app = RealTimeAPI()
        self.app = FastAPI()
        self.client = ClientController()
        self.route()

    # HTTP ROUTE
    def route(self):
        @self.app.get('/')
        def rootPage():
            print("RootPage Excuted")
            return 
        
        # 영상을 뿌리기
        @self.app.get("/video_feed")
        async def video_feed():
            # 함수 주소 받아오기
            vc = self.client.get_video_controller()
            return StreamingResponse(vc.get_frame(), media_type="multipart/x-mixed-replace;boundary=frame")

        # 드론한테 video 받기
        @self.rt_app.post("/video_recv")
        def video_getter(frame):
            vc = self.client.get_video_controller()
            vc.recv_video(frame)
            return
        
        # 앱으로 key값 받기
        @self.rt_app.post("/key_apk")
        def change_key(key):
            # 함수 주소 받아오기
            pc = self.client.get_pilot_controller()
            pc.try_recv_control(key)
            return

        # 드론한테 key값 보내기
        @self.rt_app.get("/key_drone")
        def get_key():
            # 함수 주소 받아오기
            pc = self.client.get_pilot_controller()
            data = pc.try_recv_control()
            parser = Parser()  # data = "key x1 y1 x2 y2"
            parsed_data = parser.run(head="key", list_data=data)
            parser = None
            return parsed_data
        
        @self.rt_app.get("/return_apk")
        def get_latency():
            return

    # 서버 시작
    def run_server(self):
        rt_thread = None
        dr_thread = None
        try :
            apk_thread:Thread = mingcorn.run(
                app=self.rt_app, host=HOST, port=RT_PORT_APK)
            dr_thread:Thread = mingcorn.run(
                app=self.rt_app, host=HOST, port=RT_PORT_DR)
            apk_thread.start() # apk socket
            dr_thread.start() # dr socket
            uvicorn.run(self.app, host=HOST, port=PORT) # HTTP
        except Exception as e:
            print(e)
        finally:
            if rt_thread:
                apk_thread.join()
                dr_thread.join()
            raise "Sytem Terminate"

