import os
import json
from pydantic import BaseModel

from shared.util import get_data_dir


class Settings(BaseModel):
    chat_name: str
    profile: str


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
        return Settings(chat_name="first", profile="default")
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
