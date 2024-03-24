from fastapi import FastAPI
import uvicorn

HOST = '127.0.0.1'
PORT = 5000

app = FastAPI()


@app.get('/')
def main():
    return "hello world"


uvicorn.run(app, host=HOST, port=PORT)

