from typing import Optional
from string import ascii_lowercase, ascii_uppercase


def validation(func):
    def inner(*args: list, **kwargs) -> Optional[bool]:
        validation_lambda = lambda arg: all([symbol in ascii_lowercase + ascii_uppercase for symbol in str(arg)])

        for arg in args:
            print("checking", arg)
            if validation_lambda(arg):
                continue

            raise ValueError(f"Argument value {arg} is not in latin")

        for arg in kwargs.values():
            print("checking", arg)
            if validation_lambda(arg):
                continue

            raise ValueError(f"Argument value {arg} is not in latin")

        func()

    return inner

@validation
def test(*args):
    return None


for values in (["a", "b"], ["1", "c"], "a", "1", ["1", "2"]):
    try:
        test(*values)
        print(values, "correct")
    except ValueError as e:
        print(values, "incorrect", e)

try:
    test(abc="abc")
    print("correct")
    test(abc={})
    print("correct")
except Exception as e:
    print(e)
