import asyncio
import sys

from loader import bot, dp, group, private


async def main():
    sys.path.append('.')  # fix relative imports

    bot_user = await bot.get_me()
    
    import app
    import handlers
    import middlewares

    handlers.setup(group, private)
    middlewares.setup(group, private)

    print(f'"{bot_user.full_name}" loaded. v{app.version}')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
