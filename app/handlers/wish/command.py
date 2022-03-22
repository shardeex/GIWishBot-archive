from aiogram import types
from app.schema import Player

#from modules import wish
from app import cache


@cache.player_loader(with_save=True)
async def private_cmd(message: types.Message, player: Player) -> None:
    """/wish command in private scope

    Args:
        message (types.Message): message object
    """
    text = str(...)
    await message.answer(text)

@cache.player_loader(with_save=True)
async def group_cmd(message: types.Message) -> None:
    """/wish command in group scope

    Args:
        message (types.Message): message object
    """
    text = str(...)
    await message.reply(text)
