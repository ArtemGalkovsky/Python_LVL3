from typing import Union
"""
FOR LARGE SEQUENCES, like: Five(Divide(Six(Divide(Seven()))))
For simple sequences (number operator number) use task2simple.py
"""


# TODO: all methods add...
class Sequence:
  """
  Using: in print nothing to do, in other cases use 
  ". calculate()" for calculations, Example:
  a = Five(Divide(Six(Divide(Seven()))))
  a.calculate() + 5
  """

  def __init__(self, sequence) -> None:
    self.sequence = sequence

  def   calculate(self) -> Union[float, int]:
    return eval(self.sequence)

  def __str__(self) -> str:
    try:
      return str(self.calculate())
    except:
      return self.sequence


class Operation:

  def __init__(self, operation: str) -> None:
    self.operation = operation

  def __call__(self, *args) -> Sequence:
    if args:
      args = self.operation + args[0].sequence
      return Sequence(args)
    return Sequence(self.operation)


class Number:

  def __init__(self, number: int) -> None:
    self.number: str = str(number)

  def __call__(self, *args) -> Sequence:
    if args:
      args = self.number + args[0].sequence
      return Sequence(args)
    return Sequence(self.number)


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
print(Five(Divide(Six(Divide(Seven())))))

print(Five(Divide(Seven())))
