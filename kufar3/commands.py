from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="Начало"
        ),
        BotCommand(
            command="unreg",
            description="Перерегистрация"
        ),
        BotCommand(
            command="post",
            description="Помощь по созданию поста"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="posts",
            description="Управление постами"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


