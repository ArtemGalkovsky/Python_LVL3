number = input("Введите номер задания > ")

number = "5simple" if number == "simple" else int(number)

with open(f"task{number}.py") as fl:
  print(fl.read())

print("Start!")
__import__(f"task{number}")
print("Program finished!")
