task_number = int(input("Choose task number > "))

print()
with open(f"task{task_number}.py", encoding="UTF-8") as fl:
  print(fl.read())

print("start!")
__import__(f"task{task_number}")
print("program finished")