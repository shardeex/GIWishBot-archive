from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Callback(CallbackData, prefix="profile_showcase_weapon"):
    action: str

select = lambda: InlineKeyboardButton(text=_(
    'Select weapon'
    ).value, switch_inline_query_current_chat='')

cancel = lambda: InlineKeyboardButton(text=_(
    'Cancel editing'
    ).value, callback_data=Callback(action='cancel').pack())

def get():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(select(), cancel()).adjust(1, 1)
    return keyboard.as_markup()
