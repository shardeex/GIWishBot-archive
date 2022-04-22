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
    private.message.register(profile.message.main.cmd, commands=['profile'])
    group.message.register(profile.message.main.cmd, commands=['profile'])
    private.callback_query.register(
        profile.callback.main.call, profile.callback.main.filter())
    private.callback_query.register(
        profile.callback.edit.call, profile.callback.edit.filter())

    # Profile showcase handlers
    private.callback_query.register(
        profile.callback.showcase.slot.call,
        profile.callback.showcase.slot.filter())
    private.callback_query.register(
        profile.callback.showcase.character.call,
        profile.callback.showcase.character.filter())
    private.inline_query.register(
        profile.inline.showcase.character.query,
        state=profile.inline.showcase.character.state)
    private.message.register(
        profile.message.showcase.character.inline,
        state=profile.inline.showcase.character.state)
    private.callback_query.register(
        profile.callback.showcase.weapon.call,
        profile.callback.showcase.weapon.filter())
    private.inline_query.register(
        profile.inline.showcase.weapon.query,
        state=profile.inline.showcase.weapon.state)
    private.message.register(
        profile.message.showcase.weapon.inline,
        state=profile.inline.showcase.weapon.state)
