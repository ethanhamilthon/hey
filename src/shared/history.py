from pydantic import BaseModel
import json
import os
from shared.util import get_data_dir

from shared.settings import Settings


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    messages: list[ChatMessage]


def load_history(settings: Settings):
    try:
        path = os.path.join(get_data_dir(), f"{settings.chat_name}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = ChatHistory(**data)
            return history
    except FileNotFoundError:
        return ChatHistory(messages=[])
    except Exception as e:
        print(e)
        return None


def save_history(history: ChatHistory, settings: Settings):
    try:
        path = os.path.join(get_data_dir(), f"{settings.chat_name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history.model_dump(), f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(e)
