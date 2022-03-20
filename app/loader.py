from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.utils.i18n import I18n
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from filters import GroupChat, PrivateChat


bot = Bot(token=getenv("TELEGRAM_TOKEN"), parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
i18n = I18n(path="app/locales", default_locale="ru", domain="GIWishBot")

group = Router(name='group')
group.message.bind_filter(GroupChat)
private = Router(name='private')
private.message.bind_filter(PrivateChat)

dp.include_router(group)
dp.include_router(private)
