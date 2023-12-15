from db import DB
from parser import CookParser
from pprint import pprint

db = DB("cooking.db")
categories = CookParser(proxies=[]).categories

while True:
    command = "A"

    while not command.isnumeric():
        command = input("""
        Введите команду:
        1 - поиск по категории
        2 - поиск по ингредиентам
        3 - поиск по названию
        4 - выход :)
        """)

    command = int(command)

    match command:
        case 1:
            category = ""
            while category not in tuple(categories.keys()):
                print(", ".join(tuple(categories.keys())))

                category = input("Введите категорию > ").strip()

            print("Вот, что удалось найти:")
            dishes = db.get_dishes_by_category(category, categories)

            for name, description in dishes:
                print(f"{name:<100} {description}")

        case 2:
            ingredients = input("Введите ингредиенты через запятую > ").split(",")
            db.print_dishes_by_ingredients(ingredients)
        case 3:
            dish_name = input("Введите название блюда > ").strip()
            print("Требуемые ингредиенты:")
            recipes = db.get_recipes_by_dishes_name(dish_name)

            print(recipes)
            for recipe in recipes:
                print(recipe)
                for ingredient, amount in recipe:
                    print(f"{ingredient:<100} {amount}")
                print("----------------")
        case 4:
            print("Bye bye!")
            exit(0)
