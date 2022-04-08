from aiogram import Router

from . import help, inv, profile, wish


def setup(group: Router, private: Router) -> None:
    # Help handlers
    private.message.register(help.cmd, commands=['help'])

    # Wish handlers
    private.message.register(wish.cmd, commands=['wish'])
    group.message.register(wish.cmd, commands=['wish'])

    # Inv handlers
    private.message.register(inv.cmd, commands=['inv'])
    group.message.register(inv.cmd, commands=['inv'])
    private.callback_query.register(inv.call, inv.Category.filter())
    group.callback_query.register(inv.call, inv.Category.filter())

    # Profile handlers
    private.message.register(profile.cmd, commands=['profile'])
    group.message.register(profile.cmd, commands=['profile'])
