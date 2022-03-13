from aiogram import Dispatcher, Router


from . import help
from bot.filters import PrivateChat, GroupChat


def setup(dp: Dispatcher) -> None:
    """Registering module handlers (message, callback_query, etc...)

    Args:
        dp (Dispatcher): aiogram dispatcher
    """

    # Defining routers
    group = Router(name='group')
    group.message.bind_filter(GroupChat)

    private = Router(name='private')
    private.message.bind_filter(PrivateChat)

    # Help handlers
    private.message.register(help.cmd)

    # Registering routers
    dp.include_router(group)
    dp.include_router(private)
