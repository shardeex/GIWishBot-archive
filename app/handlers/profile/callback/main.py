from aiogram import html, types
from aiogram.utils.i18n.core import I18n

from app.schema import Player
from app.modules import profile
from app.keyboards.inline import profile as inline_keyboards


async def call(
    query: types.CallbackQuery,
    player: Player,
    i18n: I18n,
    callback_data: inline_keyboards.main.Callback
    ) -> None:
    match callback_data.action:  # for now it is always 'edit'
        case 'main':
            text = profile.message.main.get(
                player, html.quote(query.from_user.full_name),
                profile.showcase.load.names_for_profile(
                    i18n.current_locale, player))
            reply_markup = inline_keyboards.main.get()
            await query.message.edit_text(text, reply_markup=reply_markup)
            await query.answer()
        case 'edit':
            text = profile.message.edit.get()
            reply_markup = inline_keyboards.edit.get()
            await query.message.edit_text(text, reply_markup=reply_markup)
            await query.answer()
        case _:
            await query.answer(profile.message.invalid.get(), show_alert=True)

def filter(*args):
    return inline_keyboards.main.Callback.filter(*args)
