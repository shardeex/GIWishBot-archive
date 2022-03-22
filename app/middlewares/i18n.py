from aiogram.utils.i18n import SimpleI18nMiddleware

from app.loader import i18n


i18n_middleware = SimpleI18nMiddleware(i18n)
