from aiogram import Router

from .i18n import i18n_middleware
from .player_cache import player_cache_middleware
from .message_cleaner import message_cleaner_middleware


def setup(group: Router, private: Router) -> None:
    i18n_middleware.setup(group)
    i18n_middleware.setup(private)

    player_cache_middleware.setup(group)
    player_cache_middleware.setup(private)

    message_cleaner_middleware.setup(group)
