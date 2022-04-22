from aiogram import html, types
from aiogram.utils.i18n.core import I18n

from app.modules import profile
from app.schema import Player
from app.keyboards.inline import profile as inline_keyboards


async def call(
    query: types.CallbackQuery,
    callback_data: inline_keyboards.edit.Callback,
    player: Player,
    i18n: I18n
    ) -> None:
    match callback_data.action:
        case 'showcase':
            text = profile.message.showcase.slot.get()
            reply_markup = inline_keyboards.showcase.slot.get()
        case 'namecard':
            text = profile.message.namecard.get()
            await query.answer(text, show_alert=True)
            return
        case 'cancel':
            text = profile.message.main.get(
                player, html.quote(query.from_user.full_name),
                profile.showcase.load.names_for_profile(
                    i18n.current_locale, player))
            reply_markup = inline_keyboards.main.get()
        case _:
            await query.answer(profile.message.invalid.get(), show_alert=True)
            return

    await query.message.edit_text(text, reply_markup=reply_markup)
    await query.answer()

def filter(*args):
    return inline_keyboards.edit.Callback.filter(*args)
