"""
Реализовать классы Printer, Scaner и Xerox являются производными от класса Equipment (унаследованы от него)
Свойства класса Equipment:
name (производитель)
model (модель)
year (год выпуска)
Методы Equipment класса:
action() (что делает устройство, по умолчанию возвращает - не определено)
В классах Printer, Scaner и Xerox переопределить метод action(), в зависимости от типа устройства (Printer – печатает, Scaner – сканирует, Xerox - копирует).
"""


class Equipment:

  def __init__(self, name: str, model: str, year: int) -> None:
    self.name: str = name
    self.model: str = model
    self.year: int = year

  def action(self) -> str:
    return "не определено"

  def __str__(self) -> str:
    return f"name: {self.name}, model: {self.model}, year: {self.year}"


class Printer(Equipment):

  def __init__(self, name: str, model: str, year: int) -> None:
    super().__init__(name, model, year)

  def action(self) -> str:
    return "печатает"


class Scaner(Equipment):

  def __init__(self, name: str, model: str, year: int) -> None:
    super().__init__(name, model, year)

  def action(self) -> str:
    return "сканирует"


class Xerox(Equipment):

  def __init__(self, name: str, model: str, year: int) -> None:
    super().__init__(name, model, year)

  def action(self) -> str:
    return "копирует"


equipment = Equipment("Equ", "Equ1", 1999)
print(equipment, equipment.action())

printer = Printer("Printer", "Printer 2.0", 1960)
print(printer, printer.action())

scaner = Scaner("Scaner", "Scaner 2.0", 1970)
print(scaner, scaner.action())

xerox = Xerox("Xerox", "Xerox V100", 2100)
print(xerox, xerox.action())
