from google import genai
from google.genai.chats import types

from shared import history


class ChatProvider:
    def __init__(
        self, api_key: str, chat_history: history.ChatHistory, system_prompt: str
    ):
        self.api_key = api_key
        self.chat_history = chat_history
        self.system_prompt = system_prompt

    def simple_chat(self):
        client = genai.Client(api_key=self.api_key)
        contents = []
        for message in self.chat_history.messages:
            contents.append(
                types.Content(
                    role=message.role, parts=[types.Part(text=message.content)]
                )
            )

        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=self.system_prompt),
        )
        return response
