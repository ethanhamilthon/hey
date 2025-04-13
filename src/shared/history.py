from pydantic import BaseModel
import json
import os


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    messages: list[ChatMessage]


def create_chat_history() -> ChatHistory:
    return ChatHistory(messages=[])


def history_from_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = ChatHistory(**data)
            return history
    except FileNotFoundError:
        return create_chat_history()
    except Exception as e:
        print(e)
        return None


def history_to_file(history: ChatHistory, path: str):
    """
    Save the chat history to a JSON file
    Args:
        history (ChatHistory): The chat history to save
        path (str): The path to the JSON file
    """
    try:
        directory = os.path.dirname(path)
        # Check if the directory exists. If not, create it (and any parent directories)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history.model_dump(), f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)
