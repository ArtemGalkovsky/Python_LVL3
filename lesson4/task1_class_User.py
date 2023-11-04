from typing import Optional, Union
from hashlib import sha256


class User:
    def __init__(self, login: str, password: str, name: Optional[str] = None, email: Optional[str] = None) -> None:
        self.login = login
        self.password = sha256(password.encode("UTF-8"))
        self.name = name

        if self.validate_email(email):
            self.email = email
        else:
            raise ValueError("Email must be name@service.domain")

    # Simple checker, 1% correct
    @staticmethod
    def validate_email(email: str) -> bool:
        email = email.split("@")

        if len(email) == 2:
            return True

        return False

    def check_password(self, password: str) -> bool:
        return sha256(password.encode("UTF-8")) == self.password

    def change_password(self, current_password: str, new_password: str) -> bool:
        if sha256(current_password.encode("UTF-8")).digest() == self.password.digest():
            self.password = sha256(new_password.encode("UTF-8"))
            return True

        return False

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return None

    def __delattr__(self, var: str) -> None:
        if var in ("login", "password"):
            return None

        object.__delattr__(self, var)

    def __str__(self):
        return f"{self.login=}, {self.password=}, {self.name=}, {self.email=}"


user = User("hello", "sdf[opjkf", "dfskfd", "@mail.com")
del user.password
del user.email

print(user.change_password("jsdfojfds", "fj;fd"))
print(user.change_password("sdf[opjkf", "aaaa"))

with open("emails.txt") as fl:
    for email in fl.read().splitlines():
        try:
            user1 = User("a", "a", "a", email)
            print(email, user1)
        except Exception as e:
            print(email, e)

print(user)
