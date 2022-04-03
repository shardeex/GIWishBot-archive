from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Category(CallbackData, prefix="inv_category"):
    category: str


def get(exclude: str = 'all'):
    keyboard = InlineKeyboardBuilder()

    buttons = {
        'all': types.InlineKeyboardButton(
            text=_('All').value,
            callback_data=Category(category='all').pack()),
        'characters': types.InlineKeyboardButton(
            text=_('Characters').value,
            callback_data=Category(category='characters').pack()),
        'weapons': types.InlineKeyboardButton(
            text=_('Weapons').value,
            callback_data=Category(category='weapons').pack())
    }

    if exclude == 'all':
        keyboard.add(buttons['characters'], buttons['weapons'])
    elif exclude == 'characters':
        keyboard.add(buttons['all'], buttons['weapons'])
    elif exclude == 'weapons':
        keyboard.add(buttons['characters'], buttons['all'])

    return keyboard.as_markup()
