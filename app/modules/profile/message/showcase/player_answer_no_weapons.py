from app.loader import i18n


_ = i18n.lazy_gettext

def get() -> str:
    return _(
        's-sorry, I have no free equipable weapons...'
    ).value
