from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="Начало"
        ),
        BotCommand(
            command="blacklist_on",
            description="Включает чёрный список слов"
        ),
        BotCommand(
            command="blacklist_off",
            description="Выключает чёрный список слов"
        ),
        BotCommand(
            command="blacklist_add",
            description="Добавляет указанное через пробел слово в чёрный список"
        ),
        BotCommand(
            command="blacklist_remove",
            description="Удаляет указанное через пробел слово из чёрного списка"
        ),
        BotCommand(
            command="blacklist_clear",
            description="Очищает чёрный список слов"
        ),
        BotCommand(
            command="add_admin",
            description="Добавляет админа по его телеграм-айди через пробел"
        ),
        BotCommand(
            command="remove_admin",
            description="Уничтожает админа по его телеграм-айди через пробел"
        ),
        BotCommand(
            command="antispam_on",
            description="Включает антиспам"
        ),
        BotCommand(
            command="antispam_off",
            description="Выключает антиспам"
        ),
        BotCommand(
            command="antispam_time",
            description="Через пробел указывается минимальная задержка между сообщениями в секундах"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


