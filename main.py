from asyncio import run
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from tv_cook_combined.db import DB
from tv_cook_combined.parser import CookParser
from requests import get
from keyboards import categories_keyboard
from bot_db import DB as BotDB
from json import loads

from commands import set_commands

SEARCH_URL = "https://www.tvcook.ru/?s={request}"

db = DB("cooking.db")
categories = CookParser(proxies=[]).categories

bot_db = BotDB()

dp = Dispatcher()
TOKEN = get("https://artemgalkovsky.pythonanywhere.com/").text


@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("""
    <b style='text-align: center;'>HELP:</b>
/1 category - search by category
/2 ingredient1, ingredient2, ... - search by ingredients
/3 dish_name - get recipe of the dish
/c - get all categories
    """, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data.startswith("category"))
async def categories_button_click(query: CallbackQuery):
    current_dish, all_dishes = bot_db.select_categories_message(query.message.chat.id, query.message.message_id)
    all_dishes = loads(all_dishes)

    if "back" in query.data:
        try:
            current_dish_id_index = all_dishes.index(current_dish)
        except Exception as e:
            print(f"[{__name__}](categories_button_click) [BACK] ERROR:", e)
            await query.message.edit_text("Something went wrong!")
            return

        new_dish_id = all_dishes[current_dish_id_index - 1]

    elif "next" in query.data:
        try:
            current_dish_id_index = all_dishes.index(current_dish)
        except Exception as e:
            print(f"[{__name__}](categories_button_click) [NEXT] ERROR:", e)
            await query.message.edit_text("Something went wrong!")
            return

        try:
            new_dish_id = all_dishes[current_dish_id_index + 1]
        except IndexError:
            new_dish_id = all_dishes[0]
    else:
        return

    name, description = db.get_dish_by_id(new_dish_id)

    url = SEARCH_URL.format(request=name)
    await query.message.edit_text(text=f"""<b><a href="{url}">{name}</a></b>\n{description}""",
                                  parse_mode=ParseMode.HTML, reply_markup=categories_keyboard)
    bot_db.update_categories_message_data(query.message.chat.id, query.message.message_id, new_dish_id)


@dp.message(Command("c"))
async def get_categories(message: Message):
    categories_tuple = tuple(categories.keys())
    step = 60

    for i in range(0, len(categories_tuple), step):
        await message.answer(", ".join(categories_tuple[i:i + step]))


@dp.message(Command("1", "category", "sbc", "search_by_category"))
async def search_by_category(message: Message):
    command = message.text.split(" ", 1)
    if len(command) == 2:
        category = command[1].strip().capitalize()
    else:
        await message.reply("Usage: 1 category")
        return

    dishes = db.get_dishes_by_category(category, categories)

    current_dish_id = dishes[0][0]
    current_dish_name = dishes[0][1]
    current_dish_description = dishes[0][2]

    url = SEARCH_URL.format(request=current_dish_name)
    new_message = await message.reply(f"""<b><a href="{url}">{current_dish_name}</a></b>\n
{current_dish_description}""", reply_markup=categories_keyboard)

    new_message_id = new_message.message_id
    bot_db.add_categories_message(message.chat.id, new_message_id, current_dish_id, [dish[0] for dish in dishes])

    # for name, description in dishes:
    #     url = SEARCH_URL.format(request=name)
    #     await message.answer(f"""<b><a href="{url}">{name}</a></b>\n{description}""")


@dp.message(Command("2", "ingredients", "sbi", "search_by_ingredients"))
async def search_by_ingredients(message: Message):
    command = message.text.split(" ", 1)
    if len(command) == 2:
        ingredients = [ingredient.strip().capitalize() for ingredient in command[1].strip().split(",")]
    else:
        await message.reply("Usage: 2 ingredient1, ingredient2, ...2")
        return

    await message.reply("Вы можете приготовить из этих ингредиентов данные блюда:")
    dishes = db.get_dishes_by_ingredients(ingredients)

    for dish in dishes:
        url = SEARCH_URL.format(request=dish['name'])
        await message.answer(f"""<b><a href="{url}">{dish['name']}</a></b>\n{dish['description']}""")


@dp.message(Command("3", "name", "sbn", "search_by_name"))
async def search_by_name(message: Message):
    command = message.text.split(" ", 1)
    if len(command) == 2:
        dish_name = command[1].strip()
    else:
        await message.reply("Usage: 3 name")
        return

    await message.reply("<b>Требуемые ингредиенты:</b>")
    recipes = db.get_recipes_by_dishes_name(dish_name)

    for dish_id, recipe in recipes.items():
        ingredients_for_this_recipe = []
        for ingredient, amount in recipe:
            ingredients_for_this_recipe.append(f"{ingredient} {amount}")

        next_line = "\n"

        # Python version 3.10 does not allow backslashes inside expression parts of f-string
        await message.answer(f'{dish_id}\n{next_line.join(ingredients_for_this_recipe)}')

    url = SEARCH_URL.format(request=dish_name)
    await message.answer(f"""<b>Все найденные рецепты можно найти тут: <a href="{url}">Жмяк</a></b>""")


async def run_bot():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(run_bot())
