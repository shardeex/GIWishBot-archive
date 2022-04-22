from aiogram import html, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.i18n.core import I18n

from app.modules import profile
from app.keyboards.inline import profile as inline_keyboards
from app.schema import Player
from app.states import profile as states


async def call(
    query: types.CallbackQuery,
    callback_data: inline_keyboards.showcase.slot.Callback,
    player: Player,
    i18n: I18n,
    state: FSMContext
    ) -> None:
    match callback_data.slot:
        case "0"|"1"|"2"|"3":
            await state.set_state(states.ShowcaseEdit.character)
            await state.update_data(slot=callback_data.slot)
            text = profile.message.showcase.character.get(
                int(callback_data.slot)+1)
            reply_markup = inline_keyboards.showcase.character.get()
        case "-1":  # cancel
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
    return inline_keyboards.showcase.slot.Callback.filter(*args)
