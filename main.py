import asyncio
import os

import aiogram

from classes import Gacha, User, database

router = aiogram.Router()

gacha = Gacha()
gacha.check_images()


@router.message(aiogram.filters.Command(commands=['wish']))
async def wish(message: aiogram.types.message.Message):
    user = User(message.from_user)
    if message.chat.type == 'private':
        await message.answer(user.wish_only_in_chat())
    else:
        await user.load_from_database()
        await message.reply(gacha.wish(user))
        await user.save_to_database()

@router.message(aiogram.filters.Command(commands=['inv', 'inventory']))
async def inventory(message: aiogram.types.message.Message):
    user = User(message.from_user)
    await user.load_from_database()
    await message.answer(gacha.inventory(user))


async def main():
    await database.connect()
    bot = aiogram.Bot(token=os.getenv('TELEGRAM_TOKEN'), parse_mode='HTML')
    dispatcher = aiogram.Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
