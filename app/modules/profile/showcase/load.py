from typing import Callable

from app import genshin
from app.schema import Player
from app.modules import inv


def names_for_profile(lang: str, player: Player) -> list:
    names = []
    for slot in player.showcase:
        if slot == []:
            names.append(None)
        else:
            slot_names = []
            for item_id in slot:
                item = genshin.items[item_id]
                number = player.inventory[item_id]
                slot_names.append(item.name_with_number(lang, number))
            names.append(slot_names)
    return names

def player_items(
    player: Player,
    lang: str,
    start: int, size: int = 50,
    condition: Callable = lambda item: True,
    except_showcase: bool = True
    ) -> list[genshin.Item]:
    if except_showcase:
        inventory = set(player.inventory.keys()) ^ {i for s in player.showcase for i in s}
    else:
        inventory = set(player.inventory.keys())

    items = inv.load.items_by_condition(inventory, condition=condition)[1:]
    items = sorted([item for sublist in reversed(items) for item in sublist], key=lambda i: i.get_name(lang))

    overall_items = len(items)
    if overall_items == 0:
        return None
    elif start >= overall_items:  # done
        return []
    elif start + size >= overall_items:  # last
        return items[start:overall_items+1]
    else:
        return items[start:start+size]
