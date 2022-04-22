from types import SimpleNamespace

from aiogram.types import User

import app
from app.loader import i18n


_ = i18n.lazy_gettext

links = SimpleNamespace(
    github='https://github.com/shardeex/GIWishBot',
    amber='https://ambr.top',
    celestia='https://projectcelestia.com/',
    author='https://t.me/shardeex',
    channel='https://t.me/GIWishChannel')

def get(bot: User) -> str:
    '''_summary_

    :param User bot: _description_
    :return str: _description_
    '''
    preview = '<a href="{links.github}">\u2060</a>'.format(links=links)

    strings = (
        _(
            '<b>{bot.full_name} 🇺🇸 | @{bot.username}</b>'
            ).format(bot=bot),
        _(
            'Special thanks goes to:'
            ).value,
        _(
            '✦ <b><a href="{links.amber}">Project Amber</a></b> ' +
            'for the game data and character pictures.'
            ).format(links=links),
        _(
            '✦ <b><a href="{links.celestia}">Project Celestia</a></b> ' +
            'for weapon pictures.'
            ).format(links=links),
        _(
            '<b><a href="{links.github}">GitHub</a></b> | ' +
            '<b><a href="{links.author}">Author</a></b> | ' +
            '<b><a href="{links.channel}">Channel</a></b> | ' +
            '<b>v{version}</b>'
            ).format(links=links, version=app.__version__))

    return preview + '\n'.join(strings)
