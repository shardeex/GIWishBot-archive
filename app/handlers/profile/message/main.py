from aiogram import html, types
from aiogram.utils.i18n.core import I18n

from app.modules import profile
from app.schema import Player
from app.keyboards.inline import profile as inline_keyboards


async def cmd(
    message: types.Message,
    i18n: I18n,
    player: Player
    ) -> None:
    username = html.quote(message.from_user.full_name)

    showcase = profile.showcase.load.names_for_profile(
        i18n.current_locale, player)
    text = profile.message.main.get(player, username, showcase)

    if message.chat.type == 'private':
        reply_markup = inline_keyboards.main.get()
    else:
        reply_markup = None

    await message.reply(text, reply_markup=reply_markup)
