from google import genai
from google.genai.chats import types

from shared import history


def read_file_tool(path: str) -> str:
    """
    Read a file from a given path.
    It can be any path that python can read. Use it to read files from the filesystem.
    If user did not specified the path just read it from the current directory
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class ChatProvider:
    def __init__(
        self, api_key: str, chat_history: history.ChatHistory, system_prompt: str
    ):
        self.api_key = api_key
        self.chat_history = chat_history
        self.system_prompt = system_prompt

    def simple_chat(self):
        client = genai.Client(api_key=self.api_key)
        contents = [
            types.Content(role="user", parts=[types.Part(text=m.content)])
            for m in self.chat_history.messages
        ]

        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=self.system_prompt),
        )
        return response
