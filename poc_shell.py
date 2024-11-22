import os
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
import subprocess
import sys
import json

# Set up the Langfuse callback handler
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

langfuse_callback_handler.set_trace_params(
  user_id="user-123",
  session_id="session-abc",
  tags=["ReAct shell"]
)

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

question = sys.argv[1]
response = agent.chat(question)

print(response)

## ---- Run test success:
# (ai-automatic-env-build) ➜  ai-automatic-env-build git:(main) prunp  poc_shell.py "How many python files are there in the current directory?"
# [nltk_data] Error loading punkt_tab: <urlopen error [Errno 111]
# [nltk_data]     Connection refused>
# > Running step 71ce7891-50f2-4ca9-a84d-e18dddaa64f0. Step input: How many python files are there in the current directory?
# Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
# Action: run_shell_command
# Action Input: {'command': 'ls | grep .py | wc -l'}
# Observation: 2
# 
# > Running step 78c7656b-5404-4840-b9d1-463b1d5ce9bb. Step input: None
# Thought: I can now infer that there are 2 python files in the current directory. The conversation is complete and no further tools need to be used.
# Answer: There are 2 Python files in the current directory.
# There are 2 Python files in the current directory.
# (ai-automatic-env-build) ➜  ai-automatic-env-build git:(main) pwd
# /home/xlisp/Desktop/ai-automatic-env-build
# (ai-automatic-env-build) ➜  ai-automatic-env-build git:(main)
# 
