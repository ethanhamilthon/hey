from typing import Iterable
from openai.types.chat import ChatCompletionMessageParam
from openai.types.responses import ResponseInputParam
from shared.history import ChatHistory
from openai import OpenAI


class OpenaiProvider:
    def __init__(
        self,
        api_key: str,
        chat_history: ChatHistory,
        system_prompt: str,
        model: str,
    ):
        self.api_key = api_key
        self.chat_history = chat_history
        self.system_prompt = system_prompt
        self.model = model

    def chat(self):
        client = OpenAI(api_key=self.api_key)
        contents: Iterable[ChatCompletionMessageParam] = []
        contents.append({"role": "developer", "content": self.system_prompt})
        for m in self.chat_history.messages:
            if m.role == "user":
                contents.append({"role": "user", "content": m.content})
            else:
                contents.append({"role": "assistant", "content": m.content})

        stream = client.chat.completions.create(
            model=self.model,
            messages=contents,
            stream=True,
        )

        return stream
