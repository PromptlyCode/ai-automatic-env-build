import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
import subprocess
from flask import Flask, request
from flask_socketio import SocketIO, send
import json

from llama_index.core.callbacks import CallbackManager 
from langfuse.llama_index import LlamaIndexCallbackHandler 
# Set up the Langfuse callback handler
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])
langfuse_callback_handler.set_trace_params(
  user_id="user-123",
  session_id="session-abc",
  tags=["ReAct shell"]
)

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Define the functions to be used as tools
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b
multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b
add_tool = FunctionTool.from_defaults(fn=add)

def run_shell_command(command: str) -> str:
    """Runs a shell command and returns the output or error"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')
shell_command_tool = FunctionTool.from_defaults(fn=run_shell_command)

# Initialize the LLM and agent
llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
agent = ReActAgent.from_tools([multiply_tool, add_tool, shell_command_tool], llm=llm, verbose=True)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == "connect":
        send("Welcome to the chat!\n")
    elif message == "not-empty":
        #send("continue\n")
        print("continue")
    else:
        response = agent.chat(message)
        # Convert the response to a dictionary or string format
        response_dict = {
            "message": f'{response}'
        }
        send(json.dumps(response_dict))

# Start the Flask server with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6000)

