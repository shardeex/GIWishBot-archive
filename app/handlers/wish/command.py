from aiogram import types
from aiogram.utils.i18n.core import I18n
from app.schema import Player

from app.modules import wish


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
    name = message.from_user.full_name
    is_wish, time_left = wish.availability.check(lang, player)
    # unlimited wishes!
    # is_wish, time_left = True, 0

    if is_wish:
        item = wish.items.get(player)
        if event_chat.type != 'private':
            info = wish.items.cashback(player, item)
        else:
            info = wish.message.get_cashback_alert()
        text = wish.message.get_now(lang, player, name, item, info)
    else:
        text = wish.message.get_later(player, name, time_left)

    new_message = await message.reply(text)
    result = {}

    if is_wish:
        result['save_player'] = True
        if item.rarity == 3:  # junk
            result['clean_messages'] = [
                {'message': message, 'delay': 60},
                {'message': new_message, 'delay': 60}]
    else:
        result['save_player'] = False
        result['clean_messages'] = [
                {'message': message, 'delay': 10},
                {'message': new_message, 'delay': 10}]

    return result
