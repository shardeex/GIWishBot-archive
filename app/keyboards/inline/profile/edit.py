from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Callback(CallbackData, prefix="profile_edit"):
    action: str

showcase = lambda: InlineKeyboardButton(text=_(
    'Edit showcase'
    ).value, callback_data=Callback(action='showcase').pack())

namecard = lambda: InlineKeyboardButton(text=_(
    'Edit namecard'
    ).value, callback_data=Callback(action='namecard').pack())

cancel = lambda: InlineKeyboardButton(text=_(
    'Cancel editing'
    ).value, callback_data=Callback(action='cancel').pack())

def get():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(showcase(), namecard(), cancel()).adjust(1, 1, 1)
    return keyboard.as_markup()
