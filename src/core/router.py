from dataclasses import dataclass


@dataclass
class AppArgs:
    is_new: bool
    query: str
    last: bool
    model: str

    def __init__(
        self,
        is_new: bool = False,
        query: str = "",
        last: bool = False,
        profile: str = "",
    ):
        self.is_new = is_new
        self.query = query
        self.last = last
        self.profile = profile


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

        if arg.startswith("--profile="):
            profile = arg.split("=")[1]
            args.profile = profile
            continue

        match arg:
            case "--new":
                args.is_new = True
            case "--last":
                args.last = True
            case _:
                args.query = arg
                is_query_started = True

    return args
