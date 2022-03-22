import json

from character import Character
from weapon import Weapon


with open('app/genshin/assets/characters.json', encoding='utf-8') as file:
    characters = {str(c["id"]): Character(**c) for c in json.load(file)}

with open('app/genshin/assets/weapons.json', encoding='utf-8') as file:
    weapons = {str(w["id"]): Weapon(**w) for w in json.load(file)}

items = characters | weapons

__all__ = ['characters', 'weapons', 'items']
