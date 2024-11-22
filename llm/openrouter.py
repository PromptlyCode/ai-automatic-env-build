from typing import Dict, List, Tuple
import requests
import json

class OpenRouterLLM:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate_response(self, messages: List[Dict]) -> str:
        """
        Generate a response using the OpenRouter API.

        Args:
            messages: List of message dictionaries with role and content
        Returns:
            str: Generated response
        """
        try:
            response = requests.post(
                url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                },
                data=json.dumps({
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": messages,
                    "top_p": 1,
                    "temperature": 0.1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                    "repetition_penalty": 1,
                    "top_k": 0,
                })
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
