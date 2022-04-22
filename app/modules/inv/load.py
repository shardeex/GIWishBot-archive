from typing import Callable, cast

from app import genshin


def items_by_rarity(
    inventory: dict[str, int],
    category: str = 'all'
    ) -> list:
    items = [None, [], [], [], [], []]

    match category:
        case 'all':
            allowed_types = genshin.Character, genshin.Weapon
        case 'characters':
            allowed_types = genshin.Character,
        case 'weapons':
            allowed_types = genshin.Weapon,
        case _:
            raise ValueError(category)

    for identifier, number in inventory.items():
        item = genshin.items[identifier]
        if isinstance(item, allowed_types):
            items[item.rarity].append({'item': item, 'number': number})

    return items

def names_by_rarity(
    lang: str,
    inventory: dict[str, int] | None = None,
    items: list | None = None,
    category: str = 'all',
    extra_number: bool = False
    ) -> list[list[str]]:
    if items == None:
        if inventory == None:
            raise ValueError(inventory)
        items = items_by_rarity(inventory, category)
    
    names = [None, [], [], [], [], []]
    
    for rarity in range(5, 0, -1):
        for i in range(len(items[rarity])):
            data = items[rarity][i]
            item = cast(genshin.Character | genshin.Weapon, data['item'])
            number = cast(int, data['number'])
            names[rarity].append(
                item.name_with_number(lang, number, extra_number))
        names[rarity].sort()
    return names

def numbers_by_rarity(
    inventory: dict[str, int] | None = None,
    items: list | None = None,
    category: str = 'all',
    ) -> list[int]:
    if items == None:
        if inventory == None:
            raise ValueError(inventory)
        items = items_by_rarity(inventory, category)
    
    numbers = [None, 0, 0, 0, 0, 0]
    
    for rarity in range(5, 0, -1):
        for i in range(len(items[rarity])):
            numbers[rarity] += items[rarity][i]['number']
    
    return numbers

def items_by_condition(
    item_ids: set,
    condition: Callable = lambda *args: True
    ) -> list:
    items = [None, [], [], [], [], []]
    for identifier in item_ids:
        if condition(item := genshin.items[identifier]):
            items[item.rarity].append(item)
    return items
