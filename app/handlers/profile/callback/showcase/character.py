from aiogram import html, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.i18n.core import I18n

from app.modules import profile
from app.keyboards.inline import profile as inline_keyboards
from app.schema import Player
from app.states import profile as states


async def call(
    query: types.CallbackQuery,
    callback_data: inline_keyboards.showcase.character.Callback,
    player: Player,
    i18n: I18n,
    state: FSMContext
    ) -> None:
    match callback_data.action:
        case "clear":
            data = await state.get_data()
            slot = int(data['slot'])
            player.showcase[slot] = []
            text = profile.message.showcase.cleared_slot.get(slot+1)
            reply_markup = inline_keyboards.edit.get()
            await query.message.edit_text(text, reply_markup=reply_markup)
            await state.clear()
            return {'save_player': True}
        case "cancel":
            text = profile.message.main.get(
                player, html.quote(query.from_user.full_name),
                profile.showcase.load.names_for_profile(
                    i18n.current_locale, player))
            reply_markup = inline_keyboards.main.get()
            await state.clear()
            await query.message.edit_text(text, reply_markup=reply_markup)
        case _:
            await query.answer(profile.message.invalid.get(), show_alert=True)
    
    await query.answer()

def filter(*args):
    return inline_keyboards.showcase.character.Callback.filter(*args)
