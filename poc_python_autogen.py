import sys
import argparse
import autogen
from typing import Dict, List, Tuple
import os
import pytest
import ast
import json
from llm.openrouter import OpenRouterLLM
from cli import parse_arguments, read_requirements

class CodeProject:
    def __init__(self, workspace_dir: str, api_key: str):
        self.workspace_dir = workspace_dir
        self.llm = OpenRouterLLM(api_key)

    def get_llm_response(self, role: str, prompt: str) -> str:
        """Get response from LLM based on role and prompt."""
        system_messages = {
            "code_writer": "You are a skilled Python developer. Write clean, efficient, and well-documented code.",
            "code_reviewer": "You are a code reviewer. Analyze code for best practices, potential issues, and improvements.",
            "test_writer": "You are a test engineer. Write comprehensive unit tests and integration tests.",
            "architect": "You are a software architect. Suggest appropriate file names and project structure."
        }

        messages = [
            {"role": "system", "content": system_messages[role]},
            {"role": "user", "content": prompt}
        ]

        return self.llm.generate_response(messages)

    def validate_python_code(self, code: str) -> bool:
        """Validate if the code is syntactically correct Python code."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def write_code_to_file(self, code: str, filename: str):
        """Write code to a file in the workspace directory."""
        os.makedirs(self.workspace_dir, exist_ok=True)
        filepath = os.path.join(self.workspace_dir, filename)
        print(f"Writing code to: {filepath}")
        with open(filepath, "w") as f:
            f.write(code)

    def extract_code_from_response(self, response: str) -> str:
        """Extract code blocks from LLM response."""
        code_blocks = [
            block for block in response.split("```python")
            if block.strip() and "```" in block
        ]

        if not code_blocks:
            raise ValueError("No code was generated")

        return code_blocks[0].split("```")[0].strip()

    def suggest_file_names(self, requirements: str) -> Tuple[str, str]:
        """Get AI suggestions for appropriate file names based on requirements."""
        prompt = f"""
        Based on these project requirements, suggest appropriate Python file names for:
        1. The main implementation file
        2. The test file

        Requirements:
        {requirements}

        Respond in this format:
        main_file: suggested_name.py
        test_file: suggested_test_name.py

        Use clear, descriptive names following Python conventions.
        """

        response = self.get_llm_response("architect", prompt)

        # Parse the response to extract file names
        for line in response.split('\n'):
            if 'main_file:' in line:
                main_file = line.split(':')[1].strip()
            elif 'test_file:' in line:
                test_file = line.split(':')[1].strip()

        if not main_file.endswith('.py'):
            main_file += '.py'
        if not test_file.endswith('.py'):
            test_file += '.py'

        return main_file, test_file

    def generate_project(self, requirements: str) -> Tuple[str, str]:
        """
        Generate a complete project based on requirements.

        Args:
            requirements (str): Project requirements and specifications

        Returns:
            Tuple[str, str]: Main file name and test file name
        """
        # Get AI-suggested file names
        main_file, test_file = self.suggest_file_names(requirements)

        # Generate initial code
        code_response = self.get_llm_response(
            "code_writer",
            f"Generate Python code based on these requirements: {requirements}"
        )

        code = self.extract_code_from_response(code_response)

        if not self.validate_python_code(code):
            raise ValueError("Generated code is not valid Python")

        # Write the code to the main file
        self.write_code_to_file(code, main_file)

        # Get code review
        review_response = self.get_llm_response(
            "code_reviewer",
            f"Review this Python code:\n```python\n{code}\n```"
        )
        print("\nCode Review:")
        print(review_response)

        # Generate tests
        test_response = self.get_llm_response(
            "test_writer",
            f"Write unit tests for this code from {main_file}:\n```python\n{code}\n```"
        )

        test_code = self.extract_code_from_response(test_response)
        self.write_code_to_file(test_code, test_file)

        return main_file, test_file

    def run_tests(self, test_file: str):
        """Run the generated tests using pytest."""
        try:
            pytest.main([os.path.join(self.workspace_dir, test_file), "-v"])
        except Exception as e:
            print(f"Error running tests: {e}")

class ProjectManager:
    def __init__(self, workspace_dir: str, api_key: str):
        self.project = CodeProject(workspace_dir, api_key)

    def create_project(self, requirements: str):
        """
        Create a new project with the given requirements.

        Args:
            requirements (str): Project requirements and specifications
        """
        try:
            print("Generating project...")
            main_file, test_file = self.project.generate_project(requirements)

            print(f"\nRunning tests from {test_file}...")
            self.project.run_tests(test_file)

            print("\nProject generation completed!")
            print(f"Main implementation: {main_file}")
            print(f"Test file: {test_file}")

        except Exception as e:
            print(f"Error creating project: {e}")

def read_requirements(requirements_path: str) -> str:
    """Read requirements from file if path is provided, otherwise return the string directly."""
    if os.path.isfile(requirements_path):
        with open(requirements_path, 'r') as f:
            return f.read()
    return requirements_path

def main():
    args = parse_arguments()

    # Get API key from command line or environment
    api_key = args.api_key or os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OpenRouter API key not provided. Use --api-key or set OPENROUTER_API_KEY environment variable.")
        sys.exit(1)

    # Read requirements
    requirements = read_requirements(args.requirements)

    # Create and run project
    manager = ProjectManager(args.workspace, api_key)
    manager.create_project(requirements)

if __name__ == "__main__":
    main()
