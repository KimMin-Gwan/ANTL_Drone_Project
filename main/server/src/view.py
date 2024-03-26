from fastapi import FastAPI
from real_time_api import RealTimeAPI
import uvicorn
from constants import HOST, PORT, RT_PORT
from real_time_api import mingcorn
import threading
from threading import Thread
from fastapi.responses import StreamingResponse
from controller import VideoController


class APP_View():
    def __init__(self):
        self.RT_app = RealTimeAPI()
        self.app = FastAPI()
        self.vc = VideoController()
        self.route()

    def route(self):
        @self.app.get('/')
        def rootPage():
            print("RootPage Excuted")
            return 
        
        @self.app.get("/video_feed")
        async def video_feed():
            return StreamingResponse(self.vc.)




        
    def run_server(self):
        rt_thread = None
        try :
            rt_thread:Thread = mingcorn.run(host=HOST, port=RT_PORT)
            uvicorn.run(self.app, host=HOST, port=PORT)
        except Exception as e:
            print(e)
        finally:
            if rt_thread:
                rt_thread.join()
            raise "Sytem Terminate"





