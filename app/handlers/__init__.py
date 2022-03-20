from aiogram import Router


from . import help
from app.filters import PrivateChat, GroupChat


def setup(group: Router, private: Router) -> None:
    """Registering module handlers (message, callback_query, etc...)

    Args:
        group (Router): group & supergroup events router
        private (Router): private events router
    """

    # Help handlers
    private.message.register(help.cmd)
