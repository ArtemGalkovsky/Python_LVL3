# -*- coding: utf-8 -*-

# У Васи есть VasOS которая поддерживает файлы типа filename.extension,
# где 0 < len(filename) <= 8; 0 < len(extension) <= 3; символы filename и
# extension - латинские буквы
# Вывести количество поддерживаемых файлов


def is_latin(string: str) -> bool:
  alpha = 'abcdefghijklmnopqrstuvwxyz'

  return all(letter in alpha for letter in string)


def is_vasos_compatible_file(file: str) -> bool:
  if len(file) == 2 and 0 < len(file[0]) <= 8 and 0 < len(file[1]) <= 3 and \
  is_latin(file[0]) and is_latin(file[1]):
    return True

  return False


try:
  N = int(input())

  print(sum(is_vasos_compatible_file(input().split(".")) for i in range(N)))
except ValueError:
  print("N must be int")
