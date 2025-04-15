from pydantic import BaseModel
import os
import json

from shared.settings import Settings
from shared.util import get_data_dir


class Profile(BaseModel):
    provider: str
    model: str
    api_key: str


def get_profiles(settings: Settings):
    try:
        path = os.path.join(get_data_dir(), f"{settings.profile}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = Profile(**data)
            return history
    except FileNotFoundError:
        print("No profile found")
        return None
    except Exception as e:
        print(e)
        return None


def save_profile(profile: Profile, settings: Settings):
    try:
        path = os.path.join(get_data_dir(), f"{settings.profile}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile.model_dump(), f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(e)
