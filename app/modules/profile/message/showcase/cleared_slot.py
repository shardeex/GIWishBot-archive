from app.loader import i18n


_ = i18n.lazy_gettext

def get(slot: int) -> str:
    return _(
        'Slot #{slot} was successfully cleared.'
    ).format(slot=slot)
