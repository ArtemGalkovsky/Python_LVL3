# Кондиционер включается, если room_temperature больше 20

try:
  room_temperature = float(input())

  if room_temperature > 20:
    print("on")
  else:
    print("off")
except ValueError:
  print("Not float/int")
