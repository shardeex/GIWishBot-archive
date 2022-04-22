from app.loader import i18n


_ = i18n.lazy_gettext

def get() -> str:
    return _(
        'Sorry, but it seems that you have no free characters left.'
    ).value
