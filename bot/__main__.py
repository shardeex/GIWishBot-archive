import asyncio
import sys

from loader import bot, dp


async def main():
    sys.path.append('.')  # fix relative imports
    
    import handlers
    handlers.setup(dp)

    print('Bot loaded.')

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
