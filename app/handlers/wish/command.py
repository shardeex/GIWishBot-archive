import asyncio

from aiogram import types
from app.schema import Player

#from app.modules import wish


async def private_cmd(message: types.Message, player: Player) -> None:
    '''/wish command in private scope

    :param types.Message message: user's message
    :param Player player: player object
    '''
    text = str(player.blessing_of_the_welkin_moon)
    await asyncio.sleep(5)
    await message.answer(text)
    return {'save_player': True}

async def group_cmd(message: types.Message, player: Player) -> None:
    '''/wish command in group scope

    :param types.Message message: user's message
    :param Player player: player object
    '''
    text = str(player.blessing_of_the_welkin_moon)
    await message.reply(text)
    return {'save_player': True}
