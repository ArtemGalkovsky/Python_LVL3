# Вывести все сообщения человека из Белорусская робототехника.txt


def is_code_line(striped_line: str) -> bool:
  return striped_line.startswith("<") and striped_line.endswith(">")


# we cant use <name> in striped_code_line because +375 will be recognized as a name
# but <name> in striped_code_line.split("|")[0][1:].strip() will work
def is_username_in_code_line(striped_code_line: str, username: str) -> bool:
  return username in striped_code_line.split("|")[0][1:].strip()


with open("Белорусская робототехника.txt", encoding="UTF-8") as fl:
  line = fl.readline()

  username_to_find = input()
  print_messages = False

  while line != "":
    striped_line = line.strip()

    if is_code_line(striped_line):
      print_messages = is_username_in_code_line(striped_line, username_to_find)

    elif print_messages:
      print(striped_line)

    line = fl.readline()
