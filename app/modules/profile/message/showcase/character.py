from app.loader import i18n


_ = i18n.lazy_gettext

def get(slot: int) -> str:
    return _(
        'Selected slot #{slot}.\n'
        'Please select showcase slot character.'
    ).format(slot=slot)
