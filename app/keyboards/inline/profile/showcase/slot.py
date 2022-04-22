from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from app.loader import i18n


_ = i18n.lazy_gettext

class Callback(CallbackData, prefix="profile_showcase_slot"):
    slot: str

slot = lambda n: InlineKeyboardButton(text=_(
    'Slot #{number}'
    ).format(number=n+1), callback_data=Callback(slot=str(n)).pack())

cancel = lambda: InlineKeyboardButton(text=_(
    'Cancel editing'
    ).value, callback_data=Callback(slot=-1).pack())

def get():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(*[slot(i) for i in range(4)], cancel()).adjust(4, 1)
    return keyboard.as_markup()
