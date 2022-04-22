from aiogram import html, types
from aiogram.utils.i18n.core import I18n

from app.modules import wish
from app.schema import Player


async def cmd(
    message: types.Message,
    event_chat: types.Chat,
    i18n: I18n,  # for correct image language
    player: Player
    ) -> dict[str, bool]:
    '''/wish command

    :param types.Message message: user's message
    :param Player player: player object
    '''
    lang = i18n.current_locale
    username = html.quote(message.from_user.full_name)
    is_wish, time_left = wish.availability.check(lang, player)
    # unlimited wishes!
    is_wish, time_left = True, 0

    if is_wish:
        item = wish.items.get(player)
        if event_chat.type != 'private':
            info = wish.items.cashback(player, item)
        else:
            info = wish.message.get_cashback_alert()
        text = wish.message.get_now(lang, player, username, item, info)
    else:
        text = wish.message.get_later(player, username, time_left)

    new_message = await message.reply(text)

    if is_wish:
        return {'save_player': True}
    else:
        return {
            'clean_messages': [
                {'message': message, 'delay': 10},
                {'message': new_message, 'delay': 10}]
            }
