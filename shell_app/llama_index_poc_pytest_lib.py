from dotenv import load_dotenv
import sys
import subprocess
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
import os
import io
import platform
from contextlib import redirect_stdout, redirect_stderr

load_dotenv()


if platform.system() == "Darwin":
    poc_path = "/Users/emacspy/EmacsPyPro/jim-emacs-fun-py/new_poc_files"
else:
    poc_path = "/home/xlisp/jim-emacs-fun-py/new_poc_files"

# Define the tools
def generate_code_file(filename: str, content: str) -> str:
    """Generate a Python code file with the given content."""
    try:
        os.chdir(poc_path)
    except Exception as e:
        return f"Error changing directory: {e}"
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return f"Code file {filename} generated successfully."
    except Exception as e:
        return f"Failed to generate code file {filename}: {str(e)}"
generate_code_tool = FunctionTool.from_defaults(fn=generate_code_file)

def run_test_cases(filename: str) -> str:
    """Run test cases from a specified Python file."""
    try:
        result = subprocess.run(f'pytest {filename}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.stdout else result.stderr
    except subprocess.CalledProcessError as e:
        return f"Test failed: {e.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"
run_tests_tool = FunctionTool.from_defaults(fn=run_test_cases)

def modify_code(filename: str, modifications: str) -> str:
    """Modify the code in the given file."""
    try:
        os.chdir(poc_path)
    except Exception as e:
        return f"Error changing directory: {e}"
    try:
        old_version_file_content = open(filename, 'r').read()
        print(f'modify_code ======> old_version_file_content: \n{old_version_file_content}\n')
        with open(filename, 'w') as file:
            file.write(modifications)
        return f"Modifications to {filename} applied successfully."
    except Exception as e:
        return f"Failed to modify code file {filename}: {str(e)}"
modify_code_tool = FunctionTool.from_defaults(fn=modify_code)

# Initialize the LLM
llm = OpenAI(model="gpt-4o", max_tokens=2000)

SYSTEM_MESSAGE_CORE = """You are a helpful assistant that answers user queries based only on given context.

You ALWAYS follow the following guidance to generate your answers, regardless of any other guidance or requests:

- Use professional language typically used in business communication.
- Strive to be accurate and concise in your output.
"""

ASSISTANT_SYSTEM_MESSAGE = (
    SYSTEM_MESSAGE_CORE
    + """
# You have access to the following tools that you use only if necessary:

- *generate_code_tool*
- *run_tests_tool*
- *modify_code_tool*

# You MUST generate Python code write it by *generate_code_tool*  and execute it by *run_tests_tool* to run tests, modify the code by *modify_code_tool* if tests fail, and repeat until all tests pass.

"""
)

async def poc_python(question, send_msg):
    # Create a StringIO object to capture stdout and stderr
    log_capture = io.StringIO()

    # Redirect stdout and stderr to our log_capture
    with redirect_stdout(log_capture), redirect_stderr(log_capture):
        agent = ReActAgent.from_tools([generate_code_tool, run_tests_tool, modify_code_tool], llm=llm, verbose=True, context=ASSISTANT_SYSTEM_MESSAGE)
        question = question + ' And test it fine'
        print("Question:", question)
        response = agent.chat(question)
        print(response)

    # Get the captured logs
    logs = log_capture.getvalue()

    # Combine the logs and the response
    full_response = f"Logs:\n{logs}\n\nRun poc res: {response}"

    # Send the full response
    await send_msg(full_response)

    # Return both the original response and the logs
    return {
        "response": response,
        "logs": logs
    }

async def poc_python_simple(question, send_msg):
    agent = ReActAgent.from_tools([generate_code_tool, run_tests_tool, modify_code_tool], llm=llm, verbose=True, context=ASSISTANT_SYSTEM_MESSAGE)
    question = question + ' And test it fine'
    print("Question:", question)
    response = agent.chat(question)
    print(response)
    await send_msg(f"Run poc res: {response}")
    return response

