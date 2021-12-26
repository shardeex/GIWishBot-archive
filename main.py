import asyncio

import aiogram

import utils
from user import User, database
from images import Images


bot = aiogram.Bot(token=utils.TELEGRAM_TOKEN, parse_mode='HTML')

en_wish_command = aiogram.types.bot_command.BotCommand(command='wish', description='Barbatos, hear our wishes!')
en_inventory_command = aiogram.types.bot_command.BotCommand(command='inv', description='Time toheck your backpack')

ru_wish_command = aiogram.types.bot_command.BotCommand(command='wish', description='Барбатос, услышь наши молитвы!')
ru_inventory_command = aiogram.types.bot_command.BotCommand(command='inv', description='Время проверить свой рюкзак')

private_scope = aiogram.types.bot_command_scope_all_private_chats.BotCommandScopeAllPrivateChats()
group_scope = aiogram.types.bot_command_scope_all_group_chats.BotCommandScopeAllGroupChats()

router = aiogram.Router()
Images().update()


@router.message(aiogram.filters.Command(commands=['wish']))
async def wish(message: aiogram.types.message.Message):
    user = User(message.from_user)
    await user.load_from_database()
    await message.answer(user.wish(message.chat.type))
    await user.save_to_database()

@router.message(aiogram.filters.Command(commands=['inv']))
async def inventory(message: aiogram.types.message.Message):
    user = User(message.from_user)
    await user.load_from_database()
    await message.answer(user.inv(message.chat.type))
    await user.save_to_database()

async def main():
    await database.connect()

    # en commands
    await bot.set_my_commands([en_wish_command, en_inventory_command], scope=group_scope, language_code='en')
    await bot.set_my_commands([en_inventory_command], scope=private_scope, language_code='en')
    # ru commands
    await bot.set_my_commands([ru_wish_command, ru_inventory_command], scope=group_scope, language_code='ru')
    await bot.set_my_commands([ru_inventory_command], scope=private_scope, language_code='ru')

    dispatcher = aiogram.Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
