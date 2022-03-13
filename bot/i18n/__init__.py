import json


locales: dict[str, dict] = {}
for lang in ('en', 'ru'):
    locales[lang] = {}
    with open(f'bot/data/i18n/{lang}.json', encoding='utf-8') as f:
        dictionary: dict[str, dict[str, str]] = json.load(f)
        for category, data in dictionary.items():
            for key, value in data.items():
                locales[lang][f'{category}:{key}'] = str(value)


def get(path: str, lang: str) -> str:
    """Get localized string.

    Args:
        path (str): string path, e.g. 'message:help'
        lang (str): e.g. 'en', 'ru'

    Returns:
        str: localized string or warning string (if not found)
    """
    return locales.get(lang, locales['en']).get(path, path)
