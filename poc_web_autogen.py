import sys
import argparse
import os
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
import subprocess
import pytest
from llm.openrouter import OpenRouterLLM
from cli import parse_arguments, read_requirements

@dataclass
class WebComponent:
    html: str
    css: str
    javascript: str
    tests: str

class WebProject:
    def __init__(self, workspace_dir: str, api_key: str):
        self.workspace_dir = workspace_dir
        self.llm = OpenRouterLLM(api_key)

    def get_llm_response(self, role: str, prompt: str) -> str:
        """Get response from LLM based on role and prompt."""
        system_messages = {
            "web_developer": "You are a skilled frontend web developer. Write clean, efficient, and well-documented HTML, CSS, and JavaScript code.",
            "ui_designer": "You are a UI designer. Create modern, responsive, and accessible web designs.",
            "test_engineer": "You are a frontend test engineer. Write comprehensive Jest tests for JavaScript code and UI components.",
            "architect": "You are a frontend architect. Suggest appropriate file structure and component organization."
        }

        messages = [
            {"role": "system", "content": system_messages[role]},
            {"role": "user", "content": prompt}
        ]

        return self.llm.generate_response(messages)

    def extract_code_blocks(self, response: str) -> Dict[str, str]:
        """Extract different types of code blocks from LLM response."""
        code_blocks = {}
        current_block = None
        current_content = []

        for line in response.split('\n'):
            if line.startswith('```'):
                if current_block:
                    code_blocks[current_block] = '\n'.join(current_content)
                    current_block = None
                    current_content = []
                else:
                    block_type = line.replace('```', '').strip().lower()
                    if block_type in ['html', 'css', 'javascript', 'js', 'jest']:
                        current_block = 'javascript' if block_type in ['js', 'jest'] else block_type
            elif current_block:
                current_content.append(line)

        if current_block:
            code_blocks[current_block] = '\n'.join(current_content)

        return code_blocks

    def setup_project_structure(self) -> Tuple[str, str, str, str]:
        """Create project directory structure and return file paths."""
        os.makedirs(self.workspace_dir, exist_ok=True)

        # Create directories
        src_dir = os.path.join(self.workspace_dir, 'src')
        test_dir = os.path.join(self.workspace_dir, 'tests')
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

        # Define file paths
        html_file = os.path.join(src_dir, 'index.html')
        css_file = os.path.join(src_dir, 'styles.css')
        js_file = os.path.join(src_dir, 'app.js')
        test_file = os.path.join(test_dir, 'app.test.js')

        return html_file, css_file, js_file, test_file

    def generate_web_component(self, requirements: str) -> WebComponent:
        """Generate HTML, CSS, JavaScript and tests based on requirements."""
        # Generate HTML
        html_prompt = f"""
        Create a modern, responsive HTML structure for these requirements:
        {requirements}

        Include proper meta tags, semantic HTML5 elements, and accessibility attributes.
        Respond with only the HTML code block.
        """
        html_response = self.get_llm_response("web_developer", html_prompt)
        html_code = self.extract_code_blocks(html_response).get('html', '')

        # Generate CSS
        css_prompt = f"""
        Create responsive CSS styles for this HTML:
        ```html
        {html_code}
        ```
        Based on these requirements:
        {requirements}

        Use modern CSS features, flexbox/grid, and mobile-first approach.
        Include media queries for responsiveness.
        """
        css_response = self.get_llm_response("ui_designer", css_prompt)
        css_code = self.extract_code_blocks(css_response).get('css', '')

        # Generate JavaScript
        js_prompt = f"""
        Create JavaScript code to implement the interactive functionality for:
        {requirements}

        Work with this HTML:
        ```html
        {html_code}
        ```

        Use modern JavaScript (ES6+) features and best practices.
        Include error handling and input validation.
        """
        js_response = self.get_llm_response("web_developer", js_prompt)
        js_code = self.extract_code_blocks(js_response).get('javascript', '')

        # Generate Tests
        test_prompt = f"""
        Write Jest tests for this JavaScript code:
        ```javascript
        {js_code}
        ```

        Include:
        - Unit tests for functions
        - DOM manipulation tests
        - Event handling tests
        - Error cases
        - Mock API calls if needed
        """
        test_response = self.get_llm_response("test_engineer", test_prompt)
        test_code = self.extract_code_blocks(test_response).get('javascript', '')

        return WebComponent(html_code, css_code, js_code, test_code)

    def write_files(self, component: WebComponent, file_paths: Tuple[str, str, str, str]):
        """Write generated code to files."""
        html_file, css_file, js_file, test_file = file_paths

        # Write HTML
        with open(html_file, 'w') as f:
            f.write(component.html)

        # Write CSS
        with open(css_file, 'w') as f:
            f.write(component.css)

        # Write JavaScript
        with open(js_file, 'w') as f:
            f.write(component.javascript)

        # Write Tests
        with open(test_file, 'w') as f:
            f.write(component.tests)

    def setup_testing_environment(self):
        """Set up Jest and necessary dependencies for testing."""
        package_json = {
            "name": "web-project",
            "version": "1.0.0",
            "scripts": {
                "test": "jest"
            },
            "devDependencies": {
                "jest": "^29.0.0",
                "jest-environment-jsdom": "^29.0.0",
                "@babel/preset-env": "^7.20.0"
            },
            "jest": {
                "testEnvironment": "jsdom"
            }
        }

        # Write package.json
        with open(os.path.join(self.workspace_dir, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)

        # Install dependencies
        subprocess.run(['npm', 'install'], cwd=self.workspace_dir)

    def run_tests(self):
        """Run Jest tests."""
        try:
            subprocess.run(['npm', 'test'], cwd=self.workspace_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running tests: {e}")

class WebProjectManager:
    def __init__(self, workspace_dir: str, api_key: str):
        self.project = WebProject(workspace_dir, api_key)

    def create_project(self, requirements: str):
        """Create a new web project with the given requirements."""
        try:
            print("Setting up project structure...")
            file_paths = self.project.setup_project_structure()

            print("Generating web components...")
            component = self.project.generate_web_component(requirements)

            print("Writing files...")
            self.project.write_files(component, file_paths)

            print("Setting up testing environment...")
            self.project.setup_testing_environment()

            print("Running tests...")
            self.project.run_tests()

            print("\nProject generation completed!")
            print(f"Project location: {self.project.workspace_dir}")

        except Exception as e:
            print(f"Error creating project: {e}")

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
    manager = WebProjectManager(args.workspace, api_key)
    manager.create_project(requirements)

if __name__ == "__main__":
    main()
