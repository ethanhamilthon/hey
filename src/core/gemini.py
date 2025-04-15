from google import genai
from google.genai.chats import types

from shared import history


class GeminiProvider:
    def __init__(
        self,
        api_key: str,
        chat_history: history.ChatHistory,
        system_prompt: str,
        model: str,
    ):
        self.api_key = api_key
        self.chat_history = chat_history
        self.system_prompt = system_prompt
        self.model = model

    def simple_chat(self):
        client = genai.Client(api_key=self.api_key)
        contents = [
            types.Content(role="user", parts=[types.Part(text=m.content)])
            for m in self.chat_history.messages
        ]

        response = client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=self.system_prompt),
        )
        return response
