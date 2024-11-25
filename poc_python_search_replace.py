import autogen
from typing import List, Tuple, Dict
import re
import tempfile
import os
import pytest
import shutil
import requests
import json
from llm.openrouter import OpenRouterLLM

class CustomAssistantAgent(autogen.AssistantAgent):
    def __init__(self, name: str, llm_config: dict, openrouter_llm: OpenRouterLLM):
        super().__init__(name=name, llm_config=llm_config)
        self.openrouter_llm = openrouter_llm

    def generate_reply(self, messages: List[Dict]):
        """Override the default generate_reply to use OpenRouterLLM"""
        try:
            response = self.openrouter_llm.generate_response(messages)
            return response
        except Exception as e:
            print(f"Error generating reply: {e}")
            return None

class CodeModifier:
    def __init__(self, api_key: str):
        # Initialize OpenRouterLLM
        self.llm = OpenRouterLLM(api_key)

        # Configure the assistant and user proxies
        self.assistant = CustomAssistantAgent(
            name="assistant",
            llm_config={
                "temperature": 0.1,
            },
            openrouter_llm=self.llm
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "workspace"},
        )

    def apply_diff(self, file_path: str, diff_block: str) -> bool:
        """Apply a single diff block to the code file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Parse the diff block
            search_pattern = re.search(r'<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE',
                                    diff_block, re.DOTALL)

            if not search_pattern:
                return False

            search_code = search_pattern.group(1)
            replace_code = search_pattern.group(2)

            # Apply the replacement
            new_content = content.replace(search_code, replace_code)

            # Write the modified content
            with open(file_path, 'w') as f:
                f.write(new_content)

            return True
        except Exception as e:
            print(f"Error applying diff: {e}")
            return False

    def run_tests(self, test_file: str) -> Tuple[bool, str]:
        """Run pytest and return results."""
        try:
            pytest.main(["-v", test_file])
            return True, "Tests passed"
        except Exception as e:
            return False, str(e)

    def process_code(self, problem_description: str, target_files: List[str], max_iterations: int = 5) -> bool:
        """Main workflow to process code modifications and testing."""

        # Create a temporary working directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy target files to workspace
            for file_path in target_files:
                shutil.copy(file_path, temp_dir)

            iteration = 0
            while iteration < max_iterations:
                # Generate conversation messages
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

                        Use this diff format:
                        <<<<<<< SEARCH
                        (original code)
                        =======
                        (modified code)
                        >>>>>>> REPLACE
                        """
                    }
                ]

                # Initiate the conversation
                chat_response = self.user_proxy.initiate_chat(
                    self.assistant,
                    messages=messages
                )

                # Extract diff blocks and test code
                diff_blocks = self._extract_diff_blocks(chat_response)
                test_code = self._extract_test_code(chat_response)

                # Apply diffs to each file
                for file_path in target_files:
                    for diff in diff_blocks:
                        self.apply_diff(os.path.join(temp_dir, os.path.basename(file_path)), diff)

                # Write test file
                test_file_path = os.path.join(temp_dir, "test_generated.py")
                with open(test_file_path, 'w') as f:
                    f.write(test_code)

                # Run tests
                success, test_output = self.run_tests(test_file_path)
                if success:
                    # Copy modified files back to original location
                    for file_path in target_files:
                        shutil.copy(
                            os.path.join(temp_dir, os.path.basename(file_path)),
                            file_path
                        )
                    return True

                iteration += 1
                print(f"Iteration {iteration}: Tests failed, generating new modifications...")

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
        # Look for code blocks containing pytest
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

    success = modifier.process_code(problem, target_files)
    print(f"Code modification {'succeeded' if success else 'failed'}")
