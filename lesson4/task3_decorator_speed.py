from datetime import datetime
from time import sleep


def speed(count: int):
    def wrapper(func):
        def inner(*args, **kwargs) -> None:
            results = []
            for i in range(count):
                start = datetime.now()
                func(*args, *kwargs)
                end = datetime.now()
                results.append((end - start).total_seconds())

            print(f"avg time is {sum(results) / count}s!")

        return inner

    return wrapper


@speed(1)
def sleep_test(amount: float) -> None:
    sleep(amount)


sleep_test(1)
sleep_test(10)
