class RealString(str):
    def __init__(self, string: str) -> None:
        super().__init__()

    def __eq__(self, other: str) -> bool:
        return len(self) == len(other)

    def __ne__(self, other: str) -> bool:
        return len(self) != len(other)

    def __lt__(self, other: str) -> bool:
        return len(self) < len(other)

    def __gt__(self, other: str) -> bool:
        return len(self) > len(other)

    def __le__(self, other: str) -> bool:
        return len(self) <= len(other)

    def __ge__(self, other: str) -> bool:
        return len(self) >= len(other)


real_string = RealString("hello")
real_string1 = RealString("hello")
print(real_string == real_string1)
print(real_string != real_string1)
print(real_string < "Hi")
print(real_string > "Hi")
print(real_string <= "hello")
print(real_string >= "Hi")
