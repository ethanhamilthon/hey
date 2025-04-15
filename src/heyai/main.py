import sys

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from nanoid import generate

from core.chat import ChatProvider
from core.openai import OpenaiProvider
from core.router import router
from heyai.system import SYSTEM_PROMPT
from shared.history import (
    ChatHistory,
    ChatMessage,
    load_history,
    save_history,
)
from shared.profiles import Profile, get_profiles, save_profile
from shared.settings import Settings, get_settings, save_settings


def load_data():
    settings = get_settings()
    if not settings:
        return None
    data = load_history(settings)
    if not data:
        return None
    return settings, data


def save_data(history: ChatHistory, settings: Settings, profile: Profile):
    save_history(history, settings)
    save_profile(profile, settings)
    save_settings(settings)


def main():
    # load data
    res = load_data()
    if not res:
        print("Some error occurred while loading data")
        return
    settings, chat_history = res
    args = router(sys.argv[1:])
    if not args:
        print("Some error occurred while parsing arguments")
        return

    if args.profile != "":
        settings.profile = args.profile

    profile = get_profiles(settings)
    if not profile:
        print("No profile found")
        return

    if args.is_new:
        print("New chat started")
        chat_history = ChatHistory(messages=[])
        settings.chat_name = generate()
        if args.query == "":
            save_data(chat_history, settings, profile)
            return

    if args.last:
        if len(chat_history.messages) != 0:
            md = Markdown(chat_history.messages[-1].content, code_theme="dracula")
            panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
            console = Console()
            console.print(panel)
            return

    # chat with gemini
    chat_history.messages.append(ChatMessage(role="user", content=args.query))

    buffer = ""
    if profile.provider == "gemini":
        print("Chatting with gemini")
        chat = ChatProvider(profile.api_key, chat_history, SYSTEM_PROMPT, profile.model)
        response = chat.simple_chat()

        # print response as markdown
        buffer = ""
        md = Markdown(buffer, code_theme="dracula")
        panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
        with Live(panel, console=Console(), refresh_per_second=10) as live:
            for chunk in response:
                buffer += chunk.text or ""
                md = Markdown(buffer, code_theme="dracula")
                panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
                live.update(panel)
    elif profile.provider == "openai":
        chat = OpenaiProvider(
            profile.api_key, chat_history, SYSTEM_PROMPT, profile.model
        )
        response = chat.chat()

        # print response as markdown
        buffer = ""
        md = Markdown(buffer, code_theme="dracula")
        panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
        with Live(panel, console=Console(), refresh_per_second=10) as live:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    buffer += chunk.choices[0].delta.content or ""
                    md = Markdown(buffer, code_theme="dracula")
                    panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
                    live.update(panel)

    # save json history
    chat_history.messages.append(ChatMessage(role="assistant", content=buffer))
    save_data(chat_history, settings, profile)


if __name__ == "__main__":
    main()
