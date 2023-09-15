# Заполнить список из N элементов числами. Вывести его в обратном порядке

from random import randrange

try:
  N = int(input())
  lst = [randrange(1, 1000) for num in range(N)]
  lst.reverse()

  print(lst)

except ValueError:
  print("N must be int")
