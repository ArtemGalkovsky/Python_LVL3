from asyncio import run
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from os import system
from requests import get
from bs4 import BeautifulSoup
from focast_module import get_forcast_for_town

TOKEN = get("https://artemgalkovsky.pythonanywhere.com/DefaultPassword12345").text
ZODIAC_SIGNS = {"овен": "Aries", "телец": "Taurus", "близнецы": "Gemini",
                "рак": "Cancer", "лев": "Leo", "дева": "Virgo", "весы": "Libra",
                "скорпион": "Scorpio", "стрелец": "Sagittarius", "козерог": "Capricorn",
                "водолей": "Aquarius", "рыбы": "Pisces"}

dp = Dispatcher()


def get_horoscope(symbol: str) -> str:
    print(symbol)
    response = get(f"https://horo.mail.ru/prediction/{symbol}/today/")
    html = response.content

    soup = BeautifulSoup(html, "lxml")

    print("\n".join(p.text for p in soup.select("p")[:2]))
    print(" ".join(span.text for span in soup.select(".p-score-day__item__value__inner")))

    return "\n".join(p.text for p in soup.select("p")[:2])


@dp.message(Command(*ZODIAC_SIGNS.keys()))
async def zodiac_sings(message: Message) -> None:
    horoscope = get_horoscope(ZODIAC_SIGNS[message.text.replace("/", "").strip()].lower())

    await message.reply(horoscope)


@dp.message(Command("id"))
async def start(message: Message) -> None:
    await message.answer(str(message.from_user.id), parse_mode=ParseMode.HTML)


@dp.message(Command("-pc"))
async def turn_off_pc(message: Message) -> None:
    if message.from_user.id == 1082000762:
        system("shutdown -s -t 1")


@dp.message(Command("for", "forcast"))
async def forecast(message: Message) -> None:
    text = message.text.split(" ", 1)

    if len(text) == 2:
        town = text[1]

        try:
            await message.reply(get_forcast_for_town(town))
        except:
            await message.reply("Такого города нет, ты чооо")
    else:
        await message.reply("Use /for town_name")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
