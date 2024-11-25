import autogen
from llm.openrouter import OpenRouterLLM
from typing import List, Tuple, Dict, Optional, Union

class CustomAssistantAgent(autogen.AssistantAgent):
    def __init__(self, name: str, llm_config: dict, openrouter_llm: OpenRouterLLM):
        super().__init__(name=name, llm_config=llm_config)
        self.openrouter_llm = openrouter_llm
        self.last_message_received = None

    def receive(self, message: Union[str, Dict], sender: autogen.Agent, request_reply: Optional[bool] = None, silent: Optional[bool] = False):
        """Override receive to store the last message"""
        self.last_message_received = message
        return super().receive(message, sender, request_reply, silent)

    def generate_reply(
        self,
        messages: List[Dict],
        sender: Optional[autogen.Agent] = None,
        **kwargs
    ) -> Union[str, Dict, None]:
        """Override generate_reply to use OpenRouterLLM"""
        try:
            # Only generate a response for new messages
            if isinstance(self.last_message_received, dict) and "terminate" in self.last_message_received.get("content", "").lower():
                return None

            response = self.openrouter_llm.generate_response(messages)
            return response
        except Exception as e:
            print(f"Error generating reply: {e}")
            return None

