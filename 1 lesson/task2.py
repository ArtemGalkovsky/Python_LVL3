# Кондиционер включается, если room_temperature строго больше temperature_to_set, 
# а humidity 80% или ниже.

try:
	temperature_to_set, room_temperature, humidity = map(float, input().split())
	
	if room_temperature > temperature_to_set and humidity <= 80:
		print("on")
	else:
		print("off")
except ValueError:
	print("Not float/int")
