from view.RT_APP import RealTimeAPI, mingcorn
from threading import Thread

HOST = "127.0.0.1"
PORT = 5000

class APPView():
    def __init__(self, controller):
        self.rt_app = RealTimeAPI(controller)

    def run_server(self):
        rt_thread = None

        try:
            rt_thread:Thread = mingcorn.run(
                app=self.rt_app, host=HOST, port=PORT)
            rt_thread.start()
        except Exception as e:
            print(e)
        finally:
            if rt_thread:
                rt_thread.join()
            raise "Sytem Terminate"




