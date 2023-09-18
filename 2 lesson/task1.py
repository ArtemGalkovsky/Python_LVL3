"""
Класс содержит свойства:
speed (скорость),
capacity (максимальное количество пассажиров),
maxSpeed (максимальная скорость),
passengers (количество пассажиров),
hasEmptySeats (наличие свободных мест).
Класс содержит методы:
посадка одного (по умолчанию) или нескольких пассажиров,
высадка одного (по умолчанию) или нескольких пассажиров,
увеличение скорости на заданное значение,
уменьшение скорости на заданное значение,
информация обо всем. 
"""


class Bus:

  def __init__(self, speed: float, capacity: int, maxSpeed: float,
               passengers: int) -> None:
    self.speed: float = speed
    self.capacity: int = capacity
    self.maxSpeed: float = maxSpeed
    self.passengers: int = passengers

    self.hasEmptySeats: bool = False
    self._verify_capacity()
    self._verify_speed()

  # verifying if that bus has empty seats and passengers >= 0
  def _verify_capacity(self) -> None:
    if self.passengers < 0:
      self.passengers = 0
      print("oversized leave")
      self.hasEmptySeats = False
    elif self.passengers >= self.capacity:
      print("overload")
      self.hasEmptySeats = False
      self.passengers = self.capacity

    if 0 <= self.passengers < self.capacity:
      self.hasEmptySeats = True

  # verifying if that bus speed <= max speed and speed >= 0
  def _verify_speed(self) -> None:
    if self.speed > self.maxSpeed:
      print("overspeed")
      self.speed = self.maxSpeed
    elif self.speed < 0:
      print("negative speed")
      self.speed = 0

  def add_passengers(self, number: int = 1) -> None:
    self.passengers += number
    self._verify_capacity()

  def remove_passengers(self, number: int = 1) -> None:
    self.passengers -= number
    self._verify_capacity()

  def increase_speed(self, speed: float) -> None:
    self.speed += speed
    self._verify_speed()

  def decrease_speed(self, speed: float) -> None:
    self.speed -= speed
    self._verify_speed()

  def info(self) -> str:
    information = f"\nBus stats: {self.speed=}, {self.capacity=} {self.passengers=}" +\
                  f",\n{self.maxSpeed=},{self.hasEmptySeats=}\n"
    print(information)
    return information


bus = Bus(10.0, 10, 100, 10)
bus.info()

bus.add_passengers()
print("add_passengers()", f"{bus.passengers=}")
bus.info()

bus.remove_passengers(100)
print("remove_passengers(100)", f"{bus.passengers=}")
bus.info()

bus.add_passengers(5)
print("add_passengers(5)", f"{bus.passengers=}")
bus.info()

bus.increase_speed(100)
print("increase_speed(100)", f"{bus.speed=}")
bus.info()

bus.decrease_speed(110)
print("decrease_speed(110)", f"{bus.speed=}")
bus.info()

bus.increase_speed(50)
print("increase_speed(50)", f"{bus.speed=}")
bus.info()

bus2 = Bus(speed=110, capacity=1, maxSpeed=100, passengers=10)
print(
    "Broken bus: bus2 = Bus(speed=100, capacity=1, maxSpeed=100, passengers=10)"
)
bus2.info()

bus3 = Bus(speed=-10, capacity=1, maxSpeed=100, passengers=-10)
print(
    "Broken bus: bus3 = Bus(speed=-10, capacity=1, maxSpeed=100, passengers=-10)"
)
bus3.info()
