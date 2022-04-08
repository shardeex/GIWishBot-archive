from aiogram import html, types

from app.modules import profile
from app.schema import Player


async def cmd(
    message: types.Message,
    player: Player
    ) -> dict[str, bool]:
    username = html.quote(message.from_user.full_name)

    text = profile.message.get(player, username)

    await message.reply(text)
