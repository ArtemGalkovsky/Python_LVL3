from typing import Optional


class Worker:

  def __init__(self,
               name: str,
               position: Optional[str],
               salary: float = 0) -> None:
    self.name: str = name
    self.position: Optional[str] = position
    self.salary: float = salary

  def __str__(self):
    print("Name:", self.name)
    print("Position", self.position)
    print("Salary", self.salary)

    return ""

  def __mul__(self, percent):
    percent = percent / 100
    self.salary += self.salary * percent
    return self


class Manager(Worker):

  def __init__(self, name: str, salary: float = 0, bonus: float = 25) -> None:
    super().__init__(name, "Manager", salary)
    self.bonus = bonus

  def __mul__(self, percent):
    percent = percent / 100
    bonus = self.bonus / 100
    self.salary += self.salary * percent + self.salary * bonus
    return self


worker = Worker("A", "B", 1000)
worker *= 10
print("Worker", worker)

ivan_manager = Manager("Ivan", 1700)
ivan_manager *= 3.35
print("Manager", ivan_manager)
