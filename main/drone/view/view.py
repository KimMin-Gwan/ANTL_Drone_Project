from view.RT_APP import RealTimeAPI, mingcorn
from threading import Thread

HOST = "192.168.50.227"
PORT = 5001

class APPView():
    def __init__(self, controller):
        self.rt_app = RealTimeAPI(controller)

    def run_server(self):
        rt_thread = None

        try:
            mingcorn.run(
                app=self.rt_app, host=HOST, port=PORT)
        except Exception as e:
            print(e)




