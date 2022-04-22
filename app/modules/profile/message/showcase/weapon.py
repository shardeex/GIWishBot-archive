from app.loader import i18n


_ = i18n.lazy_gettext

def get(slot: int, char_name: str) -> str:
    return _(
        'Selected <b>{char_name}</b> for slot #{slot}.\n'
        'Please select showcase slot weapon.'
    ).format(slot=slot, char_name=char_name)
