import asyncio
import sys

from database import database
from loader import bot, dp, group, private


async def main():
    sys.path.append('.')  # fix relative imports

    bot_user = await bot.me()

    import app
    # import genshin
    import handlers
    import middlewares

    handlers.setup(group, private)
    middlewares.setup(group, private)

    print(f'"{bot_user.full_name}" loaded. v{app.__version__}')
    await database.connect()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

# pybabel extract -o locales/GIWishBot.pot --input-dirs=. --project=GIWishBot --version=2.5.0a4 --msgid-bugs-address=sh4rdeex@gmail.com --copyright-holder=shardeex
# pybabel init -i locales/GIWishBot.pot -d locales -D GIWishBot -l en
# pybabel init -i locales/GIWishBot.pot -d locales -D GIWishBot -l ru
