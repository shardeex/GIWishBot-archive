from app.loader import i18n


_ = i18n.lazy_gettext

def get(slot: int, char_name: str, wepn_name: str) -> str:
    return _(
        'Successfully set <b>{char_name}</b> with <b>{wepn_name}</b> to slot #{slot}! Check your profile!'
    ).format(slot=slot, char_name=char_name, wepn_name=wepn_name)
