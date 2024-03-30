from main.server.src.view.view import APP_View

# 서버 시작

class Main:
    def run(self):
        view = APP_View()
        view.run_server()

if __name__ == "__main__":
    Main().run()

