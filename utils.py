import datetime
import json
import os
from types import SimpleNamespace

DATABASE_URL = os.getenv('DATABASE_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

REPOSITORY_NAME = 'GIWishBot'
LANGUAGE_CODES = ('en', 'ru')

with open('lang.json', mode='r', encoding='utf-8') as _l:
    languages = json.load(_l, object_hook=lambda x: SimpleNamespace(**x))

class Character(SimpleNamespace): pass
with open('characters.json', mode='r', encoding='utf-8') as _c:
    characters = json.load(_c, object_hook=lambda x: Character(**x))

class Weapon(SimpleNamespace): pass
with open('weapons.json', mode='r', encoding='utf-8') as _w:
    weapons = json.load(_w, object_hook=lambda x: Weapon(**x))

# dict with items
items_by_id = dict((item.id, item) for item in characters+weapons)

# gacha items sorted by type and rarity
_gacha_items = [i for i in weapons+characters if i.gacha]
gacha = {
    3: {
        'weapon': [i for i in _gacha_items if i.rarity == 3 and i.__class__ == Weapon]
    },
    4: {
        'weapon': [i for i in _gacha_items if i.rarity == 4 and i.__class__ == Weapon],
        'character': [i for i in _gacha_items if i.rarity == 4 and i.__class__ == Character]
    },
    5: {
        'weapon': [i for i in _gacha_items if i.rarity == 5 and i.__class__ == Weapon],
        'character': [i for i in _gacha_items if i.rarity == 5 and i.__class__ == Character]
    }
}
del _gacha_items

# probabilities to get item with given rarity in percents (0-100).
# taken as close to real values ​​as possible
drop_tables = {
    4: [x for y in [[5 for _ in range(8)], [40], [100]] for x in y],
    5: [x for y in [[1 for _ in range(73)], [7+6*j for j in range(16)], [100]] for x in y]
}

# wish times. every day users will be available to wish exactly at this time.
# e.g. datetime.time(5) means 5:00AM, datetime.time(18) means 6:00AM.
wish_times = (datetime.time(9), datetime.time(21))

# adds stardust & starglitter symbols
stardust = lambda x: f'✧{x}'
starglitter = lambda x: f'❂{x}'

def format_ru_word(number: int, word: list) -> str:
    """
    format_ru_word: formatting time to readable Russian string in
    already_wished message, for example: "1 час 2 минуты 3 секунды"
    """
    # число кончается на единицу, а десяток не равен единице (1, 21)
    if number%10 == 1 and number//10%10 != 1:
        return f'{number} {word[0]}'
    # число кончается на 2, 3, 4, а десяток не равен единице (2, 33)
    elif number%10 in (2, 3, 4) and number//10%10 != 1:
        return f'{number} {word[1]}'
    # всё остальное (5, 10, 13, 26)
    else:
        return f'{number} {word[2]}'

def format_en_word(number: int, word: list) -> str:
    """
    format_en_word: formatting time to readable English string in
    already_wished message for example: "1 hour 2 minutes 3 seconds"
    
    yeah I really like english simplicity. one or many - that's all
    """
    if number == 1:
        return f'{number} {word[0]}'
    else:
        return f'{number} {word[1]}'

def time_left_string(hour: int, minute: int, second: int, lang: str) -> str:
    """
    time_left_string: formatting time to readable string and returning it.
    """
    words = []
    if lang == 'ru':
        if hour != 0:
            words.append(format_ru_word(hour, ['час', 'часа', 'часов']))
        if minute != 0:
            words.append(format_ru_word(minute, ['минуту', 'минуты', 'минут']))
        if hour == 0:
            words.append(format_ru_word(second, ['секунду', 'секунды', 'секунд']))
    else:  # lang == 'en' or invalid
        if hour != 0:
            words.append(format_en_word(hour, ['hour', 'hours']))
        if minute != 0:
            words.append(format_en_word(minute, ['minute', 'minutes']))
        if hour == 0:
            words.append(format_en_word(second, ['second', 'seconds']))
    return ' '.join(words)

def item_name_with_replica(lang, item, count) -> str:
    """
    item_name_with_replica: returns readble name & count string
    for example: 'Lisa C5', 'Rust R3', 'Ferrous Shadow R5+17'
    """
    if item.__class__ == Character:
        return f'{getattr(item.name, lang)} C{str(count-1) if count <= 7 else "6+"+str(count-7)}'
    else:
        return f'{getattr(item.name, lang)} R{str(count) if count <= 5 else "5+"+str(count-5)}'
