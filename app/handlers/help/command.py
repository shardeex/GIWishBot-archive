from aiogram import types

from app.loader import bot
from app.modules import help


async def cmd(message: types.Message) -> dict[str, bool]:
    '''/help command

    :param types.Message message: user's message
    :param Player player: player object
    :return _type_: dict
    '''
    text = help.message.get(bot=await bot.me())
    await message.answer(text)
