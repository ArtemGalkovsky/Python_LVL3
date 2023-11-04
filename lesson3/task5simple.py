from typing import Union


class Operation:

  def __init__(self, operation: str) -> None:
    self.operation = operation

  def __call__(self, *args) -> str:
    args = self.operation + args[0]
    return args


class Number:

  def __init__(self, number: int) -> None:
    self.number: str = str(number)

  def __call__(self, *args) -> Union[str, float, int]:
    if args:
      args = self.number + args[0]
      return eval(args)
    return str(self.number)


Zero = Number(0)
One = Number(1)
Two = Number(2)
Three = Number(3)
Four = Number(4)
Five = Number(5)
Six = Number(6)
Seven = Number(7)
Eight = Number(8)
Nine = Number(9)

Add = Operation("+")
Subtract = Operation("-")
Divide = Operation("/")
Multiply = Operation("*")

print(Seven(Multiply(Five())))
print(Five(Divide(Five())))
print(Five(Divide(Seven())))
