from pydantic import BaseModel
import json
import os
from nanoid import generate


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    messages: list[ChatMessage]


class Settings(BaseModel):
    chat_name: str


def create_chat_history() -> ChatHistory:
    return ChatHistory(messages=[])


def load_history():
    try:
        settings = get_settings()
        if not settings:
            raise Exception("Settings could not be loaded")
        path = os.path.join(get_data_dir(), f"{settings.chat_name}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = ChatHistory(**data)
            return history
    except FileNotFoundError:
        return create_chat_history()
    except Exception as e:
        print(e)
        return None


def save_history(history: ChatHistory, is_new: bool):
    """
    Save the chat history to a JSON file
    Args:
        history (ChatHistory): The chat history to save
        path (str): The path to the JSON file
    """
    try:
        settings = get_settings()
        if not settings:
            raise Exception("Settings could not be loaded")
        if is_new:
            settings.chat_name = generate()
        path = os.path.join(get_data_dir(), f"{settings.chat_name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history.model_dump(), f, indent=4, ensure_ascii=False)

        save_settings(settings)
    except Exception as e:
        print(e)


def get_data_dir():
    """
    Get the path to the history file
    """
    home = os.path.expanduser("~")
    dir = os.path.join(home, ".heyai")
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def get_settings():
    """
    Get the settings json file
    """
    dir = get_data_dir()
    path = os.path.join(dir, "settings.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = Settings(**data)
            return history
    except FileNotFoundError:
        return Settings(chat_name="first")
    except Exception as e:
        print(e)
        return None


def save_settings(settings: Settings):
    """
    Save the settings to a JSON file
    Args:
        settings (Settings): The settings to save
        path (str): The path to the JSON file
    """
    try:
        dir = get_data_dir()
        path = os.path.join(dir, "settings.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings.model_dump(), f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)
