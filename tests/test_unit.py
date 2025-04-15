from core.router import AppArgs, router


def test_router():
    tests = [
        {"given": ["--new"], "expected": AppArgs(is_new=True), "eq": True},
        {
            "given": ["--profile=default"],
            "expected": AppArgs(profile="default"),
            "eq": True,
        },
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
            "given": ["--new", "--last", "hello"],
            "expected": AppArgs(query="hello", is_new=True, last=True),
            "eq": True,
        },
    ]

    for test in tests:
        if test["eq"]:
            assert router(test["given"]) == test["expected"]
        else:
            assert router(test["given"]) != test["expected"]
