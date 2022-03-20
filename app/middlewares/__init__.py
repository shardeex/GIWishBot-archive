from aiogram import Router

from .i18n import i18n_middleware


def setup(group: Router, private: Router) -> None:
    i18n_middleware.setup(group)
    i18n_middleware.setup(private)
