import datetime
import json
import random
from types import SimpleNamespace

import utils
from images import Images
from user import User


class Wishes():
    """
    
    """
    # probabilities to get item with given rarity in percents (0-100).
    # taken as close to real values ​​as possible
    four_star_drop_table = [x for y in [[5 for _ in range(8)], [40], [100]] for x in y]
    five_star_drop_table = [x for y in [[1 for _ in range(73)], [7+6*j for j in range(16)], [100]] for x in y]

    # wish times. every day users will be available to wish exactly at this time.
    # e.g. datetime.time(5) means 5:00AM, datetime.time(18) means 6:00AM.
    wish_times = (datetime.time(9), datetime.time(21))

    def __init__(self) -> None: 
        with open('data.json', encoding='utf-8', mode='r') as file:
            data_dict = json.load(file)
        
        self.data = {}
        for item_id, item_dict in data_dict.items():
            item_dict['id'] = item_id
            item_dict['image'] = {}
            item_dict['name_with_rarity'] = dict((lang, f'{item_dict["name"][lang]} {"★"*item_dict["rarity"]}') for lang in utils.LANGUAGE_CODES)
            self.data[item_id] = SimpleNamespace(**item_dict)
        
        images = Images()
        self.data = images.update_images(self.data)

        self.items = list([list([item for item in self.data.values() if (item.rarity == rarity and item.gacha)]) for rarity in range(1, 6)])
        self.items.insert(0, None)
    
    def format_ru_word(self, number: int, word: list) -> str:
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
    
    def format_en_word(self, number: int, word: list) -> str:
        """
        format_en_word: formatting time to readable English string in
        already_wished message for example: "1 hour 2 minutes 3 seconds"
        
        yeah I really like english simplicity. one or many - that's all
        """
        if number%10 == 1:
            return f'{number} {word[0]}'
        else:
            return f'{number} {word[1]}'
    
    def time_left_string(self, hour: int, minute: int, second: int, lang: str) -> str:
        """
        time_left_string: formatting time to readable string and returning it.
        """
        words = []
        if lang == 'ru':
            if hour != 0:
                words.append(self.format_ru_word(hour, ['час', 'часа', 'часов']))
            if minute != 0:
                words.append(self.format_ru_word(minute, ['минуту', 'минуты', 'минут']))
            if hour == 0:
                words.append(self.format_ru_word(second, ['секунду', 'секунды', 'секунд']))
        else:  # lang == 'en' or invalid
            if hour != 0:
                words.append(self.format_en_word(hour, ['hour', 'hours']))
            if minute != 0:
                words.append(self.format_en_word(minute, ['minute', 'minutes']))
            if hour == 0:
                words.append(self.format_en_word(second, ['second', 'seconds']))
        return ' '.join(words)
    
    def wish(self, user: User, chat_type: str) -> str:
        if chat_type == 'private':
            return user.lang.wish_in_private

        now = datetime.datetime.now()
        # creates last yesterday, all today and first tomorrow daytimes
        wish_datetimes = list(
            [datetime.datetime.combine(
                now.date() + datetime.timedelta(days=-1), self.wish_times[-1])] + \
            [datetime.datetime.combine(
                now.date(), time) for time in self.wish_times]) + \
            [datetime.datetime.combine(
                now.date() + datetime.timedelta(days=1), self.wish_times[0])]

        # finding closest datetime and checking if it's time to wish
        for i in range(len(wish_datetimes)):
            if now >= wish_datetimes[i] and now < wish_datetimes[i+1]:
                if user.last_wish > wish_datetimes[i]:
                    time_between = wish_datetimes[i+1] - now
                    h, remainder = divmod(time_between.seconds, 3600)
                    m, s = divmod(remainder, 60)
                    user.time_next_wish_left = self.time_left_string(h, m, s, user.language_code)
                    return user.lang.already_wished.format(user=user)
        
        # Comment this line to enable UNLIMITED wish
        user.last_wish = now

        # RaNdOmIsInG!!!
        if random.randint(1, 100) <= self.five_star_drop_table[user.five_star_pity]:
            user.five_star_pity = 0
            # condition prevents 5* and 4* pity overlap
            if user.four_star_pity != 10:
                user.four_star_pity += 1
            rarity = 5
        elif random.randint(1, 100) <= self.four_star_drop_table[user.four_star_pity]:
            user.five_star_pity += 1
            user.four_star_pity = 0
            rarity = 4
        else:
            user.five_star_pity += 1
            user.four_star_pity += 1
            rarity = 3
        
        # mOrE rAnDoMiSiNg
        item = random.choice(self.items[rarity])
        user.inventory.setdefault(item.id, 0)
        user.inventory[item.id] += 1

        return user.lang.wish.format(
            description=item.description[user.language_code], user=user,
            name=item.name_with_rarity[user.language_code], item=item)
    
    def item_name_with_replica(self, lang, item, count) -> str:
        """

        """
        if item.group == 'character':
            return f'{item.name[lang]} C{str(count-1) if count <= 7 else "6+"+str(count-7)}'
        else:
            return f'{item.name[lang]} R{str(count) if count <= 5 else "5+"+str(count-5)}'

    def inventory(self, user: User, chat_type: str) -> str:
        # counts every rarity items
        counts = [0, 0, 0, 0, 0, 0]
        # item strings (like "Amos' Bow R4")
        items_by_rarity = [[], [], [], [], [], []]

        for item_id, count in user.inventory.items():
            item = self.data[item_id]
            items_by_rarity[item.rarity].append(
                self.item_name_with_replica(user.language_code, item, count))
            counts[item.rarity] += count
        
        user.inventory_string = ''
        for rarity in range(len(items_by_rarity)):
            if items := sorted(items_by_rarity[rarity]):
                user.inventory_string = '\n\n' + \
                    f'{"★"*rarity} ({counts[rarity]}):\n' + \
                        ', '.join(items) + user.inventory_string
        if not user.inventory_string:
            user.inventory_string = user.lang.inventory_empty
        if chat_type == 'private':
            return user.lang.inventory_in_private.format(user=user)
        else:
            return user.lang.inventory_in_group.format(user=user)
