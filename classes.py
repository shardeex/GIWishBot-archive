import datetime
import json
import os
import random
import textwrap
from types import SimpleNamespace

import aiogram
import github
import sqlalchemy
from databases import Database
from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFont

LANGUAGES = ('en', 'ru')
with open('lang.json', encoding='utf-8', mode='r') as file:
    LANG = json.load(file)

database = Database(os.getenv('DATABASE_URL'))
# Can't load plugin: sqlalchemy.dialects:postgres ->
#  SQLAlchemy needs: sqlalchemy.dialects:postgresql
engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL').replace('postgres', 'postgresql'))
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table('users', metadata, autoload_with=engine)


class User():
    """
    Class for user representation. All data from database is stored here.
    """
    four_star_pity = 0
    five_star_pity = 0

    def __init__(self, user: aiogram.types.User):
        self.id = user.id
        self.last_wish = datetime.datetime.min
        self.inventory = {}
        self.profile = {}

        self.mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        self.lang = user.language_code if user.language_code in LANGUAGES else 'en'
    
    async def create_in_database(self):
        """
        Creates user's row in database.
        """
        await database.execute(
            users.insert().values(
                id=self.id, last_wish=self.last_wish, inventory=self.inventory,
                profile=self.profile, four_star_pity=self.four_star_pity,
                five_star_pity=self.five_star_pity))

    async def load_from_database(self):
        """
        Loads user's data from database.
        """
        if not (result := await database.fetch_one(users.select().where(users.c.id == self.id))):
            await self.create_in_database()
            result = await database.fetch_one(users.select().where(users.c.id == self.id))
        for key, value in result.items():
            setattr(self, key, value)
    
    async def save_to_database(self):
        """
        Saves user data to database.
        """
        await database.execute(
            users.update().where(users.c.id == self.id).values(
                id=self.id, last_wish=self.last_wish, inventory=self.inventory,
                profile=self.profile, four_star_pity=self.four_star_pity,
                five_star_pity=self.five_star_pity))

    def wish_only_in_chat(self):
        """
        plz be more sociable ^^
        """
        return LANG['wish_only_in_chat'][self.lang]


class Gacha():
    """
    All the magic is happening here. :D

    Drop tables, wish times, image generator, messages - e v e r y t h i n g.
    """

    # probabilities to get item with given rarity in percents (0-100).
    # taken as close to real values ​​as possible
    four_star_drop_table = [x for y in [[5 for _ in range(8)], [40], [100]] for x in y]
    five_star_drop_table = [x for y in [[1 for _ in range(73)], [7+6*j for j in range(16)], [100]] for x in y]

    # wish times. every day users will be available to wish exactly at this time.
    # e.g. datetime.time(5) means 5:00AM, datetime.time(18) means 6:00AM.
    wish_times = (datetime.time(9), datetime.time(21))

    # repository name (useful for debug)
    repo_name = 'GenshinWishBot'

    # image boxes (ye magic numbers)
    boxes = {
        'icon': (26, 279, 122, 375),
        'star': (99, 315, 121, 337),
        'character': (-192, -74, 1283, 663),
        'weapon': (372, -39, 700, 617),
        'weapon_bg': (242, -6, 831, 582),
        'weapon_shadow': (374, -27, 702, 630),
    }
    name_dot = (99, 306)
    delta_star_box = (21, 32)

    def __init__(self) -> None: 
        with open('data.json', encoding='utf-8', mode='r') as file:
            data_dict = json.load(file)
            self.data = {}

        for item_id, item_dict in data_dict.items():
            item_dict['id'] = item_id
            item = SimpleNamespace(**item_dict)
            self.data[item_id] = item

        self.drop = list([list([item for item in self.data.values() if (item.rarity == r+1 and item.gacha)]) for r in range(5)])
        self.drop.insert(0, None)

    def create_image(self, item, lang) -> None:
        """
        Generates images based on assets.
        """
        image = Image.open('assets/wishes_background.png')
        star = Image.open('assets/star.png').convert(mode='RGBA')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('assets/font.ttf', 32)

        item.box = self.boxes[item.group]
        item.size = item.box[2] - item.box[0], item.box[3] - item.box[1]

        assets = []
        
        if item.group == 'weapon':
            # weapon_bg, weapon_shadow, weapon & weapon_icon
            assets.append((
                Image.open(f'assets/weapon_bg/{item.type}.png').resize((589, 589)),
                self.boxes['weapon_bg']))
            assets.append((ImageEnhance.Brightness(
                Image.open(f'assets/{item.group}s/{item.id}.png').resize(item.size)).enhance(0.1),
                self.boxes['weapon_shadow']))
            assets.append((
                Image.open(f'assets/{item.group}s/{item.id}.png').resize(item.size),
                self.boxes['weapon']))
            assets.append((
                Image.open(f'assets/{item.group}_icon/{item.type}.png'),
                self.boxes['icon']))
        elif item.group == 'character':
            # character & element
            assets.append((
                Image.open(f'assets/{item.group}s/{item.id}.png').resize(item.size),
                self.boxes['character']))
            assets.append((
                Image.open(f'assets/element_icon/{item.element}.png'),
                self.boxes['icon']))
        else:
            raise ValueError(item)
        
        # calculate name length (rows)
        name_strings = textwrap.wrap(item.name[lang], width=15)

        # rarity stars
        for i in range(item.rarity):
            assets.append((star, (
                self.boxes['star'][0] + self.delta_star_box[0]*i,
                self.boxes['star'][1] + self.delta_star_box[1]*(len(name_strings)),
                self.boxes['star'][2] + self.delta_star_box[0]*i,
                self.boxes['star'][3] + self.delta_star_box[1]*(len(name_strings)))))
        
        # paste assets
        for asset, asset_box in assets:
            asset_with_bg = image.crop(asset_box)
            asset_with_bg.alpha_composite(asset, (0, 0))
            image.paste(asset_with_bg, asset_box)
        
        # item name
        for i in range(len(name_strings)):
            draw.text(
                (self.name_dot[0], self.name_dot[1]+i*32),
                name_strings[i], (255, 255, 255), font,
                stroke_width=1, stroke_fill=(0, 0, 0))

        profile = ImageCms.ImageCmsProfile('assets/AdobeRGB1998.icc')
        image.save(f'assets/gacha/{lang}/{item.id}.png', icc_profile=profile.tobytes())
    
    def check_images(self):
        """
        Checking images available on my own GitHub repository based on data.json.
        If image doesn't exist, creates and uploading them.
        """
        repo = github.Github(os.environ['GITHUB_TOKEN']).get_user().get_repo(self.repo_name)
        for lang in LANGUAGES:
            github_images = list([x.name[:-4] for x in repo.get_contents(f'assets/gacha/{lang}')])
            for item_id, item in self.data.items():
                item.id = item_id
                if not item.id in github_images:
                    self.create_image(item, lang)
                    repo.create_file(
                        f'assets/gacha/{lang}/{item.id}.png',
                        f'[BOT] create {item.name["en"]} picture for {lang}',
                        open(f'assets/gacha/{lang}/{item.id}.png', 'rb').read())
        
        self.__init__()
    
    def format_ru_word(self, number: int, word: list) -> str:
        """
        Formatting time to readable Russian string in already_wished message
        For example: "1 час 2 минуты 3 секунды"
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
    
    def format_en_word(self, number: int, word: list):
        """
        Formatting time to readable English string in already_wished message
        For example: "1 hour 2 minutes 3 seconds"
        
        ye I really like english simplicity. one or many - that's all
        """
        if number%10 == 1:
            return f'{number} {word[0]}'
        else:
            return f'{number} {word[1]}'
    
    def time_left_string(self, hour: int, minute: int, second: int, lang: str) -> str:
        """
        Formatting time to readable string.
        """
        words = []
        if lang == 'ru':
            if hour != 0:
                words.append(self.format_ru_word(hour, ['час', 'часа', 'часов']))
            if minute != 0:
                words.append(self.format_ru_word(minute, ['минуту', 'минуты', 'минут']))
            if second != 0:
                words.append(self.format_ru_word(second, ['секунду', 'секунды', 'секунд']))
        else:  # lang == 'en' or invalid
            if hour != 0:
                words.append(self.format_en_word(hour, ['hour', 'hours']))
            if minute != 0:
                words.append(self.format_en_word(minute, ['minute', 'minutes']))
            if second != 0:
                words.append(self.format_en_word(second, ['second', 'seconds']))
        return ', '.join(words)
    
    def wish(self, user: User) -> str:
        now = datetime.datetime.now()

        # creates today datetimes from wish times and adds one extra tommorow
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
                    time_left = self.time_left_string(h, m, s, user.lang)
                    return LANG['already_wished'][user.lang].format(mention=user.mention, time_left=time_left)
        
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
        drop = random.choice(self.drop[rarity])
        user.inventory.setdefault(drop.id, 0)
        user.inventory[drop.id] += 1

        # beautiful message and perfect image for u...
        message = LANG['wish'][user.lang].format(
            mention=user.mention,
            name=drop.name[user.lang],
            description=drop.description[user.lang],
            stars='★'*drop.rarity)
        message += f"<a href='https://raw.githubusercontent.com/shardeex/{self.repo_name}/main/assets/gacha/{user.lang}/{drop.id}.png'>⁠</a>"
        return message
    
    def inventory(self, user: User) -> str:
        # counts every rarity items
        counts = [0, 0, 0, 0, 0]
        # item strings (like "Amos' Bow R4")
        items_by_rarity = [[], [], [], [], []]

        for item_id, count in user.inventory.items():
            item = self.data[item_id]
            # constellation or refinement
            if item.group == 'character':
                str_count = f'C{str(count-1) if count <= 7 else "6+"+str(count-7)}'
            else:
                str_count = f'R{str(count) if count <= 5 else "5+"+str(count-5)}'
            items_by_rarity[item.rarity-1].append(f'{item.name[user.lang]} {str_count}')
            counts[item.rarity-1] += count
        
        inv = []
        for i in range(len(items_by_rarity)):
            stars = len(items_by_rarity)-i
            if items := sorted(items_by_rarity[stars-1]):
                inv.append(f'{"★"*stars} ({counts[stars-1]}):\n'+', '.join(items))
        if inv:
            return LANG['inventory'][user.lang].format(mention=user.mention, inventory='\n\n'.join(inv))
        else:
            return LANG['empty_inventory'][user.lang].format(mention=user.mention)
