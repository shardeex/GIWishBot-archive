from aiogram import html, types
from aiogram.utils.i18n.core import I18n
from aiogram.dispatcher.fsm.context import FSMContext

from app import genshin
from app.loader import bot
from app.modules import profile
from app.schema import Player
from app.states import profile as states
from app.keyboards.inline import profile as inline_keyboards


async def inline(
    message: types.Message,
    i18n: I18n,
    player: Player,
    state: FSMContext
    ) -> None:
    bot_user = await bot.me()

    if not message.via_bot or message.via_bot.id != bot_user.id:
        text = profile.message.via_bot.get()
        await message.reply(text)
        return

    if not message.entities:
        text = profile.message.showcase.no_weapons.get()
        reply_markup = inline_keyboards.main.get()
        await message.reply(text, reply_markup=reply_markup)
        await state.clear()
        return

    state_data = await state.get_data()
    slot = int(state_data['slot'])
    char_id = state_data['character']
    wepn_id = message.entities[0].get_text(message.text)[1:]
    await state.clear()

    # record to slot
    player.showcase[slot] = [char_id, wepn_id]

    char_name = genshin.characters[char_id].get_name(i18n.current_locale)
    wepn_name = genshin.weapons[wepn_id].get_name(i18n.current_locale)

    text = profile.message.showcase.slot_edited.get(slot+1, char_name, wepn_name)
    reply_markup = inline_keyboards.main.get_main()
    await message.reply(text, reply_markup=reply_markup)
    return {'save_player': True}
