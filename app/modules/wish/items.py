import random

from app import genshin, symbols
from app.schema import Player


# drop rates based on https://paimon.moe data
DROP_RATES = {
    4: [x for y in [[5 for _ in range(8)], [40], [100]] for x in y],
    5: [x for y in [[1 for _ in range(73)], [7+6*j for j in range(16)], [100]] for x in y]
}

def get(player: Player):
    if random.randint(1, 100) <= DROP_RATES[5][player.pities['5']['pity']]:
        rarity = 5
        player.pities['5']['pity'] = 0
        player.pities['4']['pity'] += 1

        # fixes 5★ and 4★ pity overlap
        # if 5★ on 10th 4★ pity, 4★ item will be on next pull.
        if player.pities['4']['pity'] == 10:
            player.pities['4']['pity'] -= 1

    elif random.randint(1, 100) <= DROP_RATES[4][player.pities['4']['pity']]:
        rarity = 4
        player.pities['5']['pity'] += 1
        player.pities['4']['pity'] = 0

    else:
        rarity = 3
        player.pities['5']['pity'] += 1
        player.pities['4']['pity'] += 1
    
    # https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation#Notes
    # every 270 pulls will contain both a 5★ character and weapon,
    # while every 30 pulls will have both a 4★ character and weapon.
    # UPD[RU]: https://telegra.ph/mne-len-bylo-pisat-ehto-po-anglijski-02-18
    if rarity in (4, 5):
        pity = player.pities[str(rarity)]
        if pity["twice"]:  # twice
            if pity["isweapon"]:  # twice weapon
                pity["isweapon"] = False  # character
                pity["twice"] = False  # once
                item_id = random.choice(genshin.wish_char_ids[rarity])
                item = genshin.items[item_id]
                # twice weapon -> character once
            else:  #  character
                pity["isweapon"] = True  # weapon
                pity["twice"] = False  # once
                item_id = random.choice(genshin.wish_wepn_ids[rarity])
                item = genshin.items[item_id]
                # twice character -> weapon once
        else:  # once
            item_id = random.choice(genshin.wish_item_ids[rarity])
            item = genshin.items[item_id]
            if isinstance(item, genshin.Weapon):  # new is weapon
                if pity["isweapon"] == True:  # last was also weapon
                    pity["twice"] = True  # so it's twice
                else:  # but last was character
                    pity["isweapon"] = True  # so it's weapon now 
                    pity["twice"] = False  # and once
            if isinstance(item, genshin.Character):  # new is character
                if pity["isweapon"] == False:  # last was also character
                    pity["twice"] = True  # so it's twice
                else:  # but last was not character
                    pity["isweapon"] = False  # so it's character now
                    pity["twice"] = False  # and once
    else:  # rarity = 3
        item_id = random.choice(genshin.wish_wepn_ids[rarity])
        item = genshin.items[item_id]
    
    # save item to user's inventory
    player.inventory[item_id] = player.inventory.get(item_id, 0) + 1

    return item

def cashback(player: Player, item: genshin.Weapon | genshin.Character) -> str:
    cashback = ''
    number = player.inventory[item.id]

    if item.rarity == 5:
        if isinstance(item, genshin.Character):
            if number > 1:
                if number > 7:
                    player.masterless_starglitter += 25
                    cashback = symbols.masterless_starglitter(25)
                else:
                    player.masterless_starglitter += 10
                    cashback = symbols.masterless_starglitter(10)
        elif isinstance(item, genshin.Weapon):
            player.masterless_starglitter += 10
            cashback = symbols.masterless_starglitter(10)
    elif item.rarity == 4:
        if isinstance(item, genshin.Character):
            if number > 1:
                if number > 7:
                    player.masterless_starglitter += 5
                    cashback = symbols.masterless_starglitter(5)
                else:
                    player.masterless_starglitter += 2
                    cashback = symbols.masterless_starglitter(2)
        elif isinstance(item, genshin.Weapon):
            player.masterless_starglitter += 2
            cashback = symbols.masterless_starglitter(2)
    elif item.rarity == 3:
        player.masterless_stardust += 15
        cashback = symbols.masterless_stardust(15)

    if cashback:
        cashback = f'「{cashback}」'

    return cashback
