# Функция cartesian определяет к какой четверти относятся x, y


def cartesian(x, y):
  if x > 0 and y > 0:
    return (1)
  elif x > 0 and y < 0:
    return (4)
  elif x < 0 and y > 0:
    return (2)
  else:
    return (3)


try:
  x, y = map(float, input().split())

  print(cartesian(x, y))

except ValueError:
  print("X and Y must be float")
