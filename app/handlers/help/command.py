from aiogram import types

from loader import bot, i18n
from modules import help


_ = i18n.gettext

async def cmd(message: types.Message) -> None:
    """/help command

    Args:
        message (types.Message): message object
    """
    text = help.message.get(bot=await bot.me())
    await message.answer(text)
