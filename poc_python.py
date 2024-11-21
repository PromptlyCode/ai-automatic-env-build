import sys
import subprocess
from datalog_gpt.core.agent import ReActAgent
from datalog_gpt.llms.openai import OpenAI
from datalog_gpt.core.tools import FunctionTool
import os
import platform

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

# Create the ReActAgent
agent = ReActAgent.from_tools([generate_code_tool, run_tests_tool, modify_code_tool], llm=llm, verbose=True, context=ASSISTANT_SYSTEM_MESSAGE)

# Get the question from command line arguments
question = sys.argv[1] + ' And test it fine'
print("Question:", question)

# Get the response from the agent
response = agent.chat(question)
print(response)

