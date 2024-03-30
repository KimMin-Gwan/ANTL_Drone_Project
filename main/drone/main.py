# from controller import MasterController
# from view import APPView
import controller
import view
from threading import Thread
import asyncio


class Main():
    def __init__(self):
        self.__controller = controller.MasterController()
        self.__view = view.APPView(controller=self.__controller)

    async def run(self):
        view_thread = None
        try:
            view_thread = Thread(target=self.__view.run_serve)
            view_thread.start()
            await self.__controller.run()
        except Exception as e:
            print(e)
        finally:
            if view_thread:
                view_thread.join()

if __name__ == "__main__":
    main = Main()
    asyncio.run(main.run())