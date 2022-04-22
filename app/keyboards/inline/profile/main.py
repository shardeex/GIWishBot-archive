from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Callback(CallbackData, prefix="profile"):
    action: str

main = lambda: InlineKeyboardButton(text=_(
    'Open profile'
    ).value, callback_data=Callback(action='main').pack())

edit = lambda: InlineKeyboardButton(text=_(
    'Edit profile'
    ).value, callback_data=Callback(action='edit').pack())

def get():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(edit())
    return keyboard.as_markup()

def get_main():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(main())
    return keyboard.as_markup()
