"""
Границы поля: от 0 до 100 включительно,
Робот может перемещаться 
вверх (N), вниз (S), вправо (E), влево (W).

move(directions) принимает строку – последовательность команд перемещения робота, каждая буква строки соответствует перемещению на единичный интервал в направлении, указанном буквой. Метод возвращает – конечное положение Робота (после перемещения).

path() вызывается без аргументов и возвращает список координат точек, по которым перемещался Робот при последнем вызове метода move. Если метод не вызывался, возвращает список с начальным положением Робота.
"""


class Robot:

  def __init__(self, x: int, y: int) -> None:
    self.x: int = x
    self.y: int = y
    self._verify_coordinates()

    self.robot_path = [(x, y)]

  # min(max(0, self.coord), 100) checks that coordinate >= 0 [max(0, coord)]
  # and coordinate <= 100 [min(max_coordinate, 100)]
  # if x = 110 => max(0, 110) -> 110 -> min(100, 110) -> 100
  # if x = -10 => max(0, -10) -> 0 -> min(100, 0) -> 0
  # if x = 50 => max(0, 50) -> 50 -> min(100, 50) -> 50
  def _verify_coordinates(self) -> None:
    # print("Pre verified coords", self.x, self.y)
    self.x = min(max(0, self.x), 100)
    self.y = min(max(0, self.y), 100)
    # print("Verified coords", self.x, self.y)

  def move(self, directions: str) -> tuple[int, int]:
    self.robot_path = [(self.x, self.y)]
    for direction in directions:
      if direction == "N":
        self.y += 1
      elif direction == "S":
        self.y -= 1
      elif direction == "E":
        self.x += 1
      elif direction == "W":
        self.x -= 1
      else:
        print(f"Incorrect direction: '{direction}'")
        continue

      self._verify_coordinates()
      self.robot_path.append((self.x, self.y))

    return self.x, self.y

  def path(self) -> list[tuple[int, int]]:
    return self.robot_path


x, y = map(int, input("x y > ").split())
directions = input("Directions [NSWE...] > ")

robot = Robot(x, y)

print("Coords after move:", robot.move(directions))
print("Path is", robot.path())
