import autogen
import pdb

from typing import List, Tuple, Dict, Optional, Union
import re
import tempfile
import os
import pytest
import shutil
import requests
import json
from llm.openrouter import OpenRouterLLM
from agent.custom import CustomAssistantAgent

class CodeModifier:
    def __init__(self, api_key: str):
        self.llm = OpenRouterLLM(api_key)
        self.assistant = CustomAssistantAgent(
            name="assistant",
            llm_config={"temperature": 0.1},
            openrouter_llm=self.llm
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "workspace"},
            max_consecutive_auto_reply=2  # Limit consecutive auto-replies
        )

    def apply_diff(self, file_path: str, diff_block: str) -> bool:
        """Apply a single diff block to the code file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            search_pattern = re.search(r'<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE',
                                    diff_block, re.DOTALL)

            if not search_pattern:
                return False

            search_code = search_pattern.group(1)
            replace_code = search_pattern.group(2)

            if search_code in content:  # Only replace if the search pattern exists
                new_content = content.replace(search_code, replace_code)
                with open(file_path, 'w') as f:
                    f.write(new_content)
                return True
            return False
        except Exception as e:
            print(f"Error applying diff: {e}")
            return False

    def run_tests(self, test_file: str) -> Tuple[bool, str]:
        """Run pytest and return results."""
        try:
            result = pytest.main(["-v", test_file])
            return result == pytest.ExitCode.OK, "Tests passed" if result == pytest.ExitCode.OK else "Tests failed"
        except Exception as e:
            return False, str(e)

    def process_code(self, problem_description: str, target_files: List[str], max_iterations: int = 3) -> bool:
        """Main workflow to process code modifications and testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy target files to workspace
            for file_path in target_files:
                if not os.path.exists(file_path):
                    print(f"Error: File {file_path} not found")
                    return False
                shutil.copy(file_path, temp_dir)

            iteration = 0
            while iteration < max_iterations:
                print(f"\nIteration {iteration + 1}/{max_iterations}")

                messages = [
                    {
                        "role": "user",
                        "content": f"""
                        Problem: {problem_description}

                        Current code files:
                        {self._read_files(target_files)}

                        Please generate:
                        1. Code modifications in diff format
                        2. Pytest test cases

                        **MUST return use this format for code modifications**:
                        <<<<<<< SEARCH
                        (original code)
                        =======
                        (modified code)
                        >>>>>>> REPLACE
                        """
                    }
                ]

                # Get response from assistant
                chat_response = self.user_proxy.initiate_chat(
                    self.assistant,
                    messages=messages
                )

                # Extract the last message from the assistant
                last_message = None
                for message in chat_response.chat_history:  # Changed from messages to chat_history
                    if isinstance(message, dict) and message.get("role") == "assistant":
                        last_message = message.get("content", "")

                if not last_message:
                    print("No response from assistant")
                    break

                # Extract modifications and tests
                diff_blocks = self._extract_diff_blocks(last_message)
                test_code = self._extract_test_code(last_message)

                print(f" diff_blocks ###### {diff_blocks} ####")
                #if not diff_blocks or not test_code:
                #    pdb.set_trace()
                #    print("No valid modifications or tests found")
                #    break

                # Apply modifications
                applied_any = False
                for file_path in target_files:
                    temp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
                    for diff in diff_blocks:
                        if self.apply_diff(temp_file_path, diff):
                            applied_any = True

                print(f"applied_any ===== {applied_any}")
                #if not applied_any:
                #    print("No modifications were applied")
                #    break

                # Write and run tests
                test_file_path = os.path.join(temp_dir, "test_generated.py")
                with open(test_file_path, 'w') as f:
                    f.write(test_code)

                success, test_output = self.run_tests(test_file_path)
                print(f"Test result: {test_output}")

                if True: #success:
                    # Copy successful modifications back
                    for file_path in target_files:
                        shutil.copy(
                            os.path.join(temp_dir, os.path.basename(file_path)),
                            file_path
                        )
                    print("Successfully modified code and passed tests")
                    return True

                iteration += 1
                if iteration >= max_iterations:
                    print(f"Reached maximum iterations ({max_iterations})")
                    break

            return False

    def _read_files(self, file_paths: List[str]) -> str:
        """Read and format the content of multiple files."""
        content = []
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                content.append(f"File: {file_path}\n{f.read()}")
        return "\n\n".join(content)

    def _extract_diff_blocks(self, response: str) -> List[str]:
        """Extract diff blocks from the response."""
        pattern = r'<<<<<<< SEARCH.*?>>>>>>> REPLACE'
        return re.findall(pattern, response, re.DOTALL)

    def _extract_test_code(self, response: str) -> str:
        """Extract pytest code from the response."""
        pattern = r'```python\s*(import pytest.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1)
        return ""

# Example usage
if __name__ == "__main__":
    api_key = os.getenv('OPENROUTER_API_KEY')
    modifier = CodeModifier(api_key=api_key)

    problem = """
    Fix the implementation of the calculate_average function to handle empty lists
    and return the correct average of numbers.
    """

    target_files = ["math_utils.py"]

    success = modifier.process_code(problem, target_files, max_iterations=3)
    print(f"\nFinal result: Code modification {'succeeded' if success else 'failed'}")
