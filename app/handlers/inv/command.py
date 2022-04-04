from aiogram import html, types
from aiogram.utils.i18n.core import I18n

from app.modules import inv
from app.schema import Player

from app import keyboards


async def cmd(
    message: types.Message,
    i18n: I18n,
    player: Player
    ) -> dict[str, bool]:
    '''_summary_

    :param types.Message message: _description_
    :param I18n i18n: _description_
    :param Player player: _description_
    :return dict[str, bool]: _description_
    '''
    username = html.quote(message.from_user.full_name)

    items = inv.load.items_by_rarity(player.inventory)
    names = inv.load.names_by_rarity(
        i18n.current_locale, items=items, extra_number=True)
    numbers = inv.load.numbers_by_rarity(items=items)
    text = inv.message.get(player, username, names, numbers)

    await message.reply(text, reply_markup=keyboards.inline.inv.category.get())

    return {'save_player': False}
