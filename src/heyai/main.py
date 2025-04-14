import sys
import os

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

from core.chat import ChatProvider
from heyai.system import SYSTEM_PROMPT
from shared.history import ChatHistory, ChatMessage, load_history, save_history


def get_gemini_key():
    """
    Get the API key from environment variable
    """
    key = os.getenv("HEY_GEMINI_API_KEY")
    if not key:
        return None
    return key


def main():
    # get api key
    key = get_gemini_key()
    if not key:
        print("HEY_GEMINI_API_KEY is not set")
        return

    # load json history
    chat_history = load_history()
    if not chat_history:
        print("Some error occurred while loading history")
        return

    # get text from the command line
    text = " ".join(sys.argv[1:])
    if len(sys.argv) == 1:
        print("No text provided")
        return

    # handle new conversation
    first_arg = sys.argv[1]
    if first_arg == "--new":
        print("New conversation")
        chat_history = ChatHistory(messages=[])
        if len(sys.argv) == 2:
            save_history(chat_history, True)
            return
        else:
            text = " ".join(sys.argv[2:])

    # chat with gemini
    chat_history.messages.append(ChatMessage(role="user", content=text))
    chat = ChatProvider(key, chat_history, SYSTEM_PROMPT)
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

    # save json history
    chat_history.messages.append(ChatMessage(role="assistant", content=buffer))
    save_history(chat_history, False)


if __name__ == "__main__":
    main()
