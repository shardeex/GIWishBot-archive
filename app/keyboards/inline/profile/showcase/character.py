from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Callback(CallbackData, prefix="profile_showcase_character"):
    action: str

select = lambda: InlineKeyboardButton(text=_(
    'Select character'
    ).value, switch_inline_query_current_chat='')

clear = lambda: InlineKeyboardButton(text=_(
    'Clear slot'
    ).value, callback_data=Callback(action='clear').pack())

cancel = lambda: InlineKeyboardButton(text=_(
    'Cancel editing'
    ).value, callback_data=Callback(action='cancel').pack())

def get():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(select(), clear(), cancel()).adjust(1, 1, 1)
    return keyboard.as_markup()
