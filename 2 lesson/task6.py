from random import randrange
"""
Реализовать эмулятор битвы двух солдат. Для этого нужно реализовать два класса Soldat и класс Battle

Класс Soldat содержит свойства:
name (имя солдата),
health (начальный уровень здоровья),
strength (сила удара).
Класс Soldat содержит методы:
set_name – смена имени персонажа,
make_kick – атака солдата (принимает объект противника и наносит ему урон).

Класс Battle содержит свойства:
soldat1 – принимает объект первого бойца
soldat2 – принимает объект второго бойца
result – результат последнего сражения 
Класс Battle содержит методы:
battle – моделирует сражения,
winner – возвращает имя последнего победителя.

(Повышенный уровень)
* Реализовать дополнительные особенности персонажа:
вероятность критического удара
вероятность уклонения от атаки
** 
Добавить особенность вампиризм (после успешной атаки, персонаж восстанавливает здоровье, в размере 10% от нанесенного урона).
"""


class Soldat:

  def __init__(self,
               name: str,
               health: float,
               strength: float,
               critical_damage_chance: float = 0,
               dodging_chance: float = 0):
    self.name: str = name
    self.health: float = health
    self.strength: float = strength
    self.critical_damage_chance: float = critical_damage_chance
    self.dodging_chance: float = dodging_chance

  def set_name(self, new_name: str):
    self.name = new_name

  def make_kick(self, enemy):
    critical_damage_number = randrange(0, 100)  # random percent number
    dodging_number = randrange(0, 100)  # random percent number

    # if dodgint chance = 100%, every enemy with dodge number in [0, 99] will dodge
    # if dodging chance = 0%, every enmey with dodge number in [0, 99] will not dodge
    # if dodging chance = 50%, every enemy with dodge number in [0, 49] will dodge
    # if dodging chance = 70%, every enemy with dodge number in [0, 69] will dodge
    if dodging_number < enemy.dodging_chance:
      print(enemy.name, "dodging")
    elif critical_damage_number < self.critical_damage_chance:
      enemy.health -= self.strength * 2
      self.health += 0.1 * self.strength * 2
      print("Critical damage to", enemy.name)
    else:
      print("Kicking", enemy.name)
      enemy.health -= self.strength
      self.health += 0.1 * self.strength

    print(f"{enemy.name} health is {round(enemy.health, 2)} | "
          f"{self.name} health is {round(self.health, 2)}")


class Battle:

  def __init__(self, soldat1: Soldat, soldat2: Soldat):
    self.soldat1: Soldat = soldat1
    self.soldat2: Soldat = soldat2
    self.result = "Боя ещё не было"

  def _is_one_dead(self) -> bool:
    if self.soldat1.health <= 0:
      self.result = f"Победа {self.soldat2.name}"
      return True
    elif self.soldat2.health <= 0:
      self.result = f"Победа {self.soldat1.name}"
      return True

    return False

  def battle(self):
    for i in range(randrange(3, 1000)):
      soldier_id = randrange(1, 3)

      if soldier_id == 1:
        self.soldat1.make_kick(self.soldat2)
      else:
        self.soldat2.make_kick(self.soldat1)

      if self._is_one_dead():
        break

    else:
      # the rivals are exhausted
      self.result = "Ничья"

  def winner(self):
    return self.result


warrior = Soldat(name="Warrior",
                 health=1000,
                 strength=33.3,
                 critical_damage_chance=50,
                 dodging_chance=50)
halk = Soldat(name="Halk",
              health=1000,
              strength=50,
              critical_damage_chance=50,
              dodging_chance=50)

battle = Battle(warrior, halk)
battle.battle()
print(battle.winner())
