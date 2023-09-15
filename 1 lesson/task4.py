# Телефон стоит N рублей. Маша откладывает K рублей каждый день, кроме воскресенья.
# Сколько дней ей потребуется, чтобы накопить на телефон? (Начала копить в понедельник)

try:
  N, K = map(float, input().split())

  days = 0
  while N > 0:
    days += 1
    if days % 7 != 0:
      N -= K

  print(days)
except ValueError:
  print("Not float/int")
