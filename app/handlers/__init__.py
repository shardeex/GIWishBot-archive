from aiogram import Router

from . import help, wish


def setup(group: Router, private: Router) -> None:
    # Help handlers
    private.message.register(help.cmd, commands=['help'])

    # Wish handlers
    private.message.register(wish.cmd, commands=['wish'])
    group.message.register(wish.cmd, commands=['wish'])
