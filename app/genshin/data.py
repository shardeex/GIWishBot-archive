import json

from .character import Character
from .weapon import Weapon


def get_wish_ids(items: dict[str, Character|Weapon]) -> dict[int, list[str]]:
    wish_ids = {}
    for id, item in items.items():
        if item.location == 'wish':
            try:
                wish_ids[item.rarity].append(id)
            except KeyError:
                wish_ids[item.rarity] = [id]
    return wish_ids


with open('app/genshin/assets/characters.json', encoding='utf-8') as file:
    characters = {str(c["id"]): Character(**c) for c in json.load(file)}
    wish_char_ids = get_wish_ids(characters)

with open('app/genshin/assets/weapons.json', encoding='utf-8') as file:
    weapons = {str(w["id"]): Weapon(**w) for w in json.load(file)}
    wish_wepn_ids = get_wish_ids(weapons)

items = characters | weapons
wish_item_ids = get_wish_ids(items)

__all__ = [
    'characters', 'weapons', 'items',
    'wish_char_ids', 'wish_wepn_ids', 'wish_item_ids']
