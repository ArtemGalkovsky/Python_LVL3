# В школе N учеников, вывести последовательность «на первый-второй рассчитайтесь»

try:
  N = int(input())

  for i in range(N):
    if i % 2 == 0:
      print(1, end=" ")
    else:
      print(2, end=" ")

except ValueError:
  print("N must be int")
