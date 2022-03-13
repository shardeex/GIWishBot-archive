from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

bot = Bot(token=getenv("TELEGRAM_TOKEN"), parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
