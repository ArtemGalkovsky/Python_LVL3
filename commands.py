from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="help"
        ),
        BotCommand(
            command="3",
            description="Searches dishes by name! Alias: /name /sbn /3"
        ),
        BotCommand(
            command="2",
            description="Searches dishes by ingredients in recipes! Alias: /ingredient /sbi /2"
        ),
        BotCommand(
            command="1",
            description="Searches dishes by category! Alias: /category /sbc /1"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
