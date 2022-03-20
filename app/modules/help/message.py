from loader import i18n


_ = i18n.lazy_gettext

def get():
    return _('Help message.')
