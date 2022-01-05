import datetime
import random

import aiogram
import databases
import sqlalchemy

import utils

database = databases.Database(utils.DATABASE_URL)
# Can't load plugin: sqlalchemy.dialects:postgres ->
#  SQLAlchemy needs: sqlalchemy.dialects:postgresql
engine = sqlalchemy.create_engine(utils.DATABASE_URL.replace('postgres', 'postgresql'))
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table('users', metadata, autoload_with=engine)


class User():
    """
    Class for user representation. All data from database is stored here.
    """
    
    four_star_pity = 0
    four_star_last_is_weapon = None
    four_star_last_is_twice = False

    five_star_pity = 0
    five_star_last_is_weapon = None
    five_star_last_is_twice = False

    last_wish = datetime.datetime.min

    inventory = {}
    profile = {}

    stardust = 0
    starglitter = 0

    def __init__(self, user: aiogram.types.User):
        self.id = user.id

        self.mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        self.language_code = user.language_code if user.language_code in utils.LANGUAGE_CODES else 'en'
        self.lang = getattr(utils.languages, self.language_code)

        self._dbkeys = []

    async def load_from_database(self):
        """
        load_from_database: loads user's data from database.
        """
        if not (result := await database.fetch_one(users.select().where(users.c.id == self.id))):
            # create user
            await database.execute(users.insert().values(id=self.id))
            result = await database.fetch_one(users.select().where(users.c.id == self.id))
        for key, value in result.items():
            setattr(self, key, value)
            self._dbkeys.append(key)
    
    async def save_to_database(self):
        """
        save_to_database: saves user data to database.
        """
        data = {k: getattr(self, k) for k in self._dbkeys}
        await database.execute(
            users.update().where(users.c.id == self.id).values(**data))
    
    def check_wish_available(self):
        now = datetime.datetime.now()
        # creates last yesterday, all today and first tomorrow daytimes
        wish_datetimes = list(
            [datetime.datetime.combine(
                now.date() + datetime.timedelta(days=-1), utils.wish_times[-1])] + \
            [datetime.datetime.combine(
                now.date(), time) for time in utils.wish_times]) + \
            [datetime.datetime.combine(
                now.date() + datetime.timedelta(days=1), utils.wish_times[0])]

        # finding closest datetime and checking if it's time to wish
        for i in range(len(wish_datetimes)):
            if now >= wish_datetimes[i] and now < wish_datetimes[i+1]:
                if self.last_wish > wish_datetimes[i]:
                    time_between = wish_datetimes[i+1] - now
                    h, remainder = divmod(time_between.seconds, 3600)
                    m, s = divmod(remainder, 60)
                    self.time_next_wish_left = utils.time_left_string(h, m, s, self.language_code)
                    return False
        
        # comment whis line to unlimit wishes
        self.last_wish = now
        return True
    
    def wish(self, chat_type: str) -> str:
        """
        wish: wish function... idk what to write here.
        """
        if chat_type == 'private':
            return self.lang.wish_in_private

        if not self.check_wish_available():
            return self.lang.already_wished.format(user=self)

        # RaNdOmIsInG!!!
        if random.randint(1,100) <= utils.drop_tables[5][self.five_star_pity]:
            rarity = 5
            self.five_star_pity = 0
            # fixes 5★ and 4★ pity overlap
            # if 5★ on 10th 4★ pity, 4★ item will be on next pull.
            if self.four_star_pity != 9:
                self.four_star_pity += 1
            is_twice = self.five_star_last_is_twice
            is_weapon = self.five_star_last_is_weapon

        elif random.randint(1,100) <= utils.drop_tables[4][self.four_star_pity]:
            rarity = 4
            self.five_star_pity += 1
            self.four_star_pity = 0
            is_twice = self.four_star_last_is_twice
            is_weapon = self.four_star_last_is_weapon

        else:
            rarity = 3
            self.five_star_pity += 1
            self.four_star_pity += 1
        
        # https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation#Notes
        # Every 270 pulls will contain both a 5★ character and weapon,
        # while every 30 pulls will have both a 4★ character and weapon.\
        if rarity == 4 or rarity == 5:
            if is_twice:  # twice
                if is_weapon:  # twice weapon
                    item = random.choice(utils.gacha[rarity]['character'])
                    is_weapon = False  # character
                    is_twice = False  # once
                    # twice weapon -> character once
                else:  #  character
                    item = random.choice(utils.gacha[rarity]['weapon'])
                    is_weapon = True  # weapon
                    is_twice = False  # once
                    # twice character -> weapon once
            else:  # once
                item = random.choice(utils.gacha[rarity]['character']+utils.gacha[rarity]['weapon'])
                if item.__class__ == utils.Weapon:  # new is weapon
                    if is_weapon == True:  # last was also weapon
                        is_twice = True  # so it's twice
                    else:  # but last was character
                        is_weapon = True  # so it's weapon now 
                        is_twice = False  # and once
                if item.__class__ == utils.Character:  # new is character
                    if is_weapon == False:  # last was also character
                        is_twice = True  # so it's twice
                    else:  # but last was not character
                        is_weapon = False  # so it's character now
                        is_twice = False  # and once
        else:
            item = random.choice(utils.gacha[3]['weapon'])
        
        # save item to inventory
        self.inventory.setdefault(item.id, 0)
        self.inventory[item.id] += 1
        
        # stardust and starglitter
        cashback = None
        if rarity == 5:
            self.five_star_last_is_twice = is_twice
            self.five_star_last_is_weapon = is_weapon
            if item.__class__ == utils.Character:
                if (count := self.inventory[item.id]) > 1:  # C0 - no starglitter
                    if count > 7:  # after C6
                        self.starglitter += 25
                        cashback = utils.starglitter(25)
                    else:  # C1 - C6
                        self.starglitter += 10          
                        cashback = utils.starglitter(10)
            else:  # utils.Weapon
                self.starglitter += 10
                cashback = utils.starglitter(10)

        elif rarity == 4:
            self.four_star_last_is_twice = is_twice
            self.four_star_last_is_weapon = is_weapon
            if item.__class__ == utils.Character:
                if (count := self.inventory[item.id]) > 1:  # C0 - no starglitter
                    if count > 7:  # after C6
                        self.starglitter += 5
                        cashback = utils.starglitter(5)
                    else:  # C1 - C6
                        self.starglitter += 2
                        cashback = utils.starglitter(2)           
            else:  # utils.Weapon
                self.starglitter += 2
                cashback = utils.starglitter(2)

        else:  # rarity == 3:
            self.stardust += 15
            cashback = utils.stardust(15)

        if cashback:
            info = f'{getattr(item.name, self.language_code)} {"★"*item.rarity} [{cashback}]'
        else:
            info = f'{getattr(item.name, self.language_code)} {"★"*item.rarity}'

        return self.lang.wish.format(
            description=getattr(item.description, self.language_code),
            user=self, item=item, repo=utils.REPOSITORY_NAME, info=info)
    
    def inv(self, chat_type: str) -> str:
        """
        inv: shows player inventory.
        """
        # counts every rarity items
        counts = [0, 0, 0, 0, 0, 0]
        # item strings (like "Amos' Bow R4")
        items_by_rarity = [[], [], [], [], [], []]

        # generate item strings (like "Amos' Bow R4")
        for item_id, count in self.inventory.items():
            item = utils.items_by_id[item_id]
            items_by_rarity[item.rarity].append(
                utils.item_name_with_replica(self.language_code, item, count))
            counts[item.rarity] += count
        
        # generates inv string from item list
        self.inventory_string = ''
        for rarity in range(len(items_by_rarity)):  # 0-6
            if items := sorted(items_by_rarity[rarity]):  # if any items
                self.inventory_string = '\n\n' + \
                    f'{"★"*rarity} ({counts[rarity]}):\n' + \
                        ', '.join(items) + self.inventory_string
        if not self.inventory_string:
            self.inventory_string = self.lang.inventory_empty

        if chat_type == 'private':
            return self.lang.inventory_in_private.format(user=self)
        else:
            return self.lang.inventory_in_group.format(user=self)

