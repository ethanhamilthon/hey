from core.router import AppArgs, router


def test_add():
    assert 1 + 1 == 2


def test_router():
    tests = [
        {"given": ["--new"], "expected": AppArgs(is_new=True), "eq": True},
        {"given": ["--chat"], "expected": AppArgs(chat_mode=True), "eq": True},
        {
            "given": ["hello", "world"],
            "expected": AppArgs(query="hello world"),
            "eq": True,
        },
        {
            "given": ["hello", "world"],
            "expected": AppArgs(query="hello"),
            "eq": False,
        },
        {
            "given": ["--new", "--chat", "hello"],
            "expected": AppArgs(query="hello", is_new=True, chat_mode=True),
            "eq": True,
        },
    ]

    for test in tests:
        if test["eq"]:
            assert router(test["given"]) == test["expected"]
        else:
            assert router(test["given"]) != test["expected"]
