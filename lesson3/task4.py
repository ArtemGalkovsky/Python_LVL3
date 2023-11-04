from typing import Any, Union


class Wizard(object):

  def __init__(self, name: str, rank: float, years: float) -> None:
    """
    Экземпляр класса при инициализации принимает аргументы:
    ● name (имя),
    ● rank (рейтинг),
    ● years (на какой возраст выглядит),
    """
    super().__init__()
    self.name: str = name
    self.rank: float = self.verify_rank(rank)
    self.years: float = years

  @staticmethod
  def verify_rank(rank) -> Union[float, int]:
    return min(100, max(1, rank))

  def __change_age(self, value):
    if self.years > 18:
      self.years = max(18, self.years - value)

  def change_rating(self, value: float) -> None:
    """
    change_rating(value) – изменяет рейтинг на значение value; не может
    стать больше 100 и меньше 1, изменяется только до достижения
    экстремального значения; при увеличении рейтинга уменьшается
    возраст на abs(value) // 10, но только до 18, дальше не уменьшается;
    """
    self.rank = self.verify_rank(
        value)  # Проверяем, чтобы рейтинг был между 1 и 100
    self.__change_age(abs(self.rank) // 10)  # Меняем и проверяем возраст

  def __iadd__(self, other: str):
    """
    к экземпляру класса можно прибавить строку, значение рейтинга
    увеличивается на ее длину, а возраст, соответственно, уменьшается на
    длину // 10, условия изменения такие же, как и в предыдущем пункте;
    """
    rank_string_len = len(other)
    self.rank = self.verify_rank(self.rank + rank_string_len)
    self.__change_age(abs(rank_string_len) // 10)
    return self

  def __add__(self, other: str):
    """
    к экземпляру класса можно прибавить строку, значение рейтинга
    увеличивается на ее длину, а возраст, соответственно, уменьшается на
    длину // 10, условия изменения такие же, как и в предыдущем пункте;
    """
    rank_string_len = len(other)
    self.rank = self.verify_rank(self.rank + rank_string_len)
    self.__change_age(abs(rank_string_len) // 10)
    return self.rank

  def __call__(self, argument: Union[int, float]) -> Union[float, int]:
    """
    экземпляр класса можно вызвать с аргументом-числом; возвращает
    значение: (аргумент - возраст) * рейтинг;
    """
    return (argument - self.years) * self.rank

  def __str__(self):
    return f"Wizard {self.name} with {self.rank} rating looks {self.years} years old"

  def __eq__(self, other) -> bool:
    if self.rank == other.rank and self.years == other.years and \
       len(self.name) == len(other.name):
      return True

    return False

  def __ne__(self, other) -> bool:
    if self.rank != other.rank or self.years != other.years or \
       len(self.name) != len(other.name):
      return True

    return False

  def __lt__(self, other) -> bool:
    if self.rank < other.rank or self.years < other.years or \
       len(self.name) < len(other.name):
      return True

    return False

  def __gt__(self, other) -> bool:
    if self.rank > other.rank or self.years > other.years or \
       len(self.name) > len(other.name):
      return True

    return False

  def __le__(self, other) -> bool:
    if self.rank <= other.rank or self.years <= other.years or \
       len(self.name) <= len(other.name):
      return True

    return False

  def __ge__(self, other) -> bool:
    if self.rank >= other.rank or self.years >= other.years or \
       len(self.name) >= len(other.name):
      return True

    return False


wizard = Wizard("Wizard", 110, 50)
print("wizard", wizard.name, wizard.rank, wizard.years)

wizard += "10000000000000000000"
a = wizard + "1000"
print("a = wizard + '1000'", a)
print("wizard += '10000000000000000000'; wizard = wizard + '1000' test",
      wizard.name, wizard.rank, wizard.years)

wizard.change_rating(1000)
print("change_rating(1000) test", wizard.name, wizard.rank, wizard.years)

print("__call__(110) test", wizard(110))

print("__str__ test", wizard)

print("Comparison:")
wizard1 = Wizard("Wizard", 50, 50)
wizard2 = wizard1
wizard3 = Wizard("wizard", 50, 50)
wizard4 = Wizard("WWizard", 50, 49)

print("wizard1", wizard1)
print("wizard2", wizard2)
print("wizard3", wizard3)
print("wizard4", wizard4)

print("wizard1 == wizard2", wizard1 == wizard2)
print("wizard1 == wizard3", wizard1 == wizard3)
print("wizard1 == wizard4", wizard1 == wizard4)
print()
print("wizard1 != wizard2", wizard1 != wizard2)
print("wizard1 != wizard3", wizard1 != wizard3)
print("wizard1 != wizard4", wizard1 != wizard4)
print()
print("wizard1 < wizard2", wizard1 < wizard2)
print("wizard1 < wizard3", wizard1 < wizard3)
print("wizard1 < wizard4", wizard1 < wizard4)
print()
print("wizard1 > wizard2", wizard1 > wizard2)
print("wizard1 > wizard3", wizard1 > wizard3)
print("wizard1 > wizard4", wizard1 > wizard4)
print()
print("wizard1 <= wizard2", wizard1 <= wizard2)
print("wizard1 <= wizard3", wizard1 <= wizard3)
print("wizard1 <= wizard4", wizard1 <= wizard4)
print()
print("wizard1 >= wizard2", wizard1 >= wizard2)
print("wizard1 >= wizard3", wizard1 >= wizard3)
print("wizard1 >= wizard4", wizard1 >= wizard4)
