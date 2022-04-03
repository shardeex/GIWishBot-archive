from aiogram.types import User

import app
from app.loader import i18n


_ = i18n.lazy_gettext

def get(bot: User) -> str:
    '''_summary_

    :param User bot: _description_
    :return str: _description_
    '''
    preview = '<a href="https://github.com/shardeex/GIWishBot">\u2060</a>'
    strings = (
        _('<b>{bot.full_name} 🇺🇸 | @{bot.username}</b>').format(bot=bot),
        _('Special thanks goes to:'),
        _('✦ <b><a href="ambr.top">Project Amber</a></b> ' +
            'for the game data and character pictures.'),
        _('✦ <b><a href="https://t.me/vsratoteivat">Vsratiy Teyvat</a></b> ' +
            'for the active help in bot development and testing.'),
        _('<b><a href="https://github.com/shardeex/GIWishBot">GitHub</a></b> | ' +
            '<b><a href="https://t.me/shardeex">Author</a></b> | ' +
            '<b>v{version}</b>').format(version=app.__version__)
        )
    return preview + '\n'.join(map(str, strings))
