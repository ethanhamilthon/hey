from dataclasses import dataclass


@dataclass
class AppArgs:
    is_new: bool
    query: str
    chat_mode: bool

    def __init__(self, is_new: bool = False, query: str = "", chat_mode: bool = False):
        self.is_new = is_new
        self.query = query
        self.chat_mode = chat_mode


def router(raw_args: list[str]) -> AppArgs | None:
    """
    Route the arguments to the correct function
    """
    if len(raw_args) == 0:
        return None
    args = AppArgs()
    is_query_started = False
    for arg in raw_args:
        if is_query_started:
            args.query += f" {arg}"
            continue

        match arg:
            case "--new":
                args.is_new = True
            case "--chat":
                args.chat_mode = True
            case _:
                args.query = arg
                is_query_started = True

    return args
