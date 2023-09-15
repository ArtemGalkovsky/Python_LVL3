# Создать 2 списка с рандомными значениями от 10 до 30 и в трейтий список записать
# сумму элементов каждого списка

from random import randrange


def generate_list():
  return [randrange(10, 31) for num in range(randrange(3, 100))]


lst1 = generate_list()
lst2 = generate_list()

lst3 = [sum(lst1), sum(lst2)]

print(lst1, lst2, lst3)
