from typing import Any, Optional, cast

from aiogram import types
from aiogram.utils.i18n import SimpleI18nMiddleware
from app.loader import i18n

try:
    from babel import Locale, UnknownLocaleError
except ImportError:  # pragma: no cover
    Locale = None

    class UnknownLocaleError(Exception):  # type: ignore
        pass

class FixedI18nMiddleware(SimpleI18nMiddleware):

    # Quick fix for users in group chats, who han't write to bot' dm
    async def get_locale(self, event: types.TelegramObject, data: dict[str, Any]) -> str:
        event_from_user: Optional[types.User] = data.get("event_from_user", None)
        if event_from_user is None:
            return self.i18n.default_locale
        try:
            locale = Locale.parse(event_from_user.language_code, sep="-")
            if locale is None:  # no data from Telegram about locale
                raise UnknownLocaleError()  # and return default
        except UnknownLocaleError:
            return self.i18n.default_locale
        
        if locale.language not in self.i18n.available_locales:
            return self.i18n.default_locale
        return cast(str, locale.language)

i18n_middleware = FixedI18nMiddleware(i18n)
