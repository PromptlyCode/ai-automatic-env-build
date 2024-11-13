# server.py
import socketio
import os
import platform

from functools import partial
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import aiohttp
import json
import asyncio

# import poc file:
from shell_app.llama_index_poc_pytest_lib import poc_python

# set aiohttp client timeout
aiohttp.ClientTimeout(total=20)


class StaticFilesWithoutCaching(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


# Create a new Async Server
socketio_server = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*", transports=["websocket"]
)

# Create a FastAPI app
app = FastAPI()

# Attach the server to the FastAPI app
sio_app = socketio.ASGIApp(socketio_server, other_asgi_app=app)

# -----
static_dir = os.path.join(os.path.dirname(__file__), "static")

# _app = FastAPI()
app.mount("/static", StaticFilesWithoutCaching(directory=static_dir), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/index")
async def index():
    with open(os.path.join(static_dir, "index.html")) as f:
        return HTMLResponse(content=f.read())


# app = socketio.ASGIApp(socketio_server, _app)

# ----


# Event handler for a new connection
@socketio_server.event
async def connect(sid, environ):
    print(f"Client {sid} connected")
    await socketio_server.emit("message", "Welcome!", room=sid)


async def run_shell_command(command):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, executable='/bin/bash'
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

async def run_command_dynamic_log(command, callback):
    process = await asyncio.create_subprocess_exec(
        # *command, # # 数组转字符连起来。
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    while True:
        line = await process.stdout.readline()
        if not line and process.stdout.at_eof():
            break
        if line:
            print(line.decode().strip())
            await callback(line.decode().strip())

    await process.wait()
    return process.returncode

if platform.system() == "Darwin":
    pyenv = "source /opt/anaconda3/etc/profile.d/conda.sh &&  conda activate dlcss  && PYTHONPATH='.:/Users/emacspy/FaceMashPro/datalog-llm-code-semantic-search' /opt/anaconda3/bin/poetry run "
else:
    pyenv = "source /home/xlisp/anaconda3/etc/profile.d/conda.sh &&  conda activate dlcss  && PYTHONPATH='.:/home/xlisp/datalog-llm-code-semantic-search' /home/xlisp/anaconda3/bin/poetry run "

# Event handler for receiving a message
@socketio_server.event
async def message(sid, data):
    async def send_msg(msg):
        await socketio_server.emit("response", msg, room=sid)

    #
    print(
        f"Message from {sid}: {data}"
    )  # => 接受到客户端消息，"Message from fwY_tCKp49C807vDAAAB: Hello, Server!"

    if isinstance(data, str):
        # cljs 端传入是str的json
        cmd_args = json.loads(str(data))
    else:
        # py 客户端传入的是json能自动解析: data 直接自动解析了为了dict => {'cmd': 'poc', 'question': 'write python script , need async run shell'}
        cmd_args = data
    cmd = cmd_args["cmd"]
    # TODO: question缺失问题
    question = cmd_args["question"]

    if cmd == "connected":
        print(f"Connected success!")
        await send_msg(f"Connected success!")
    elif cmd == "poc":
        await send_msg(f"run {cmd} ..... {question}")
        await poc_python(question, send_msg)
    elif cmd == "poc_shell":
        await send_msg(f"run {cmd} ..... {question}")
        # TODO
    else:
        print(f"Unsupport {cmd}")
        await send_msg(f"Unsupport {cmd}")


# Event handler for disconnection
@socketio_server.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")


# To run the server with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(sio_app, host="0.0.0.0", port=8000)
