from aiogram import Router


from . import help, wish
from app.filters import PrivateChat, GroupChat, Command


def setup(group: Router, private: Router) -> None:
    """Registering module handlers (message, callback_query, etc...)

    Args:
        group (Router): group & supergroup events router
        private (Router): private events router
    """

    # Help handlers
    private.message.register(help.cmd, commands=['help'])

    # Wish handlers
    private.message.register(wish.private_cmd, commands=['wish'])
    group.message.register(wish.group_cmd, commands=['wish'])
