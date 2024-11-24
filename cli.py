import os
import argparse

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate and test code projects')
    parser.add_argument(
        '--requirements', '-r',
        type=str,
        required=True,
        help='Path to requirements file or direct requirements string'
    )
    parser.add_argument(
        '--workspace', '-w',
        type=str,
        default='coding_workspace',
        help='Directory for generated code and tests (default: coding_workspace)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenRouter API key (optional, can also use OPENROUTER_API_KEY env var)'
    )
    return parser.parse_args()

def read_requirements(requirements_path: str) -> str:
    """Read requirements from file if path is provided, otherwise return the string directly."""
    if os.path.isfile(requirements_path):
        with open(requirements_path, 'r') as f:
            return f.read()
    return requirements_path
