import aiogram
import databases
import datetime
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
    five_star_pity = 0

    def __init__(self, user: aiogram.types.User):
        self.id = user.id
        self.last_wish = datetime.datetime.min
        self.inventory = {}
        self.profile = {}

        self.mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        self.language_code = user.language_code if user.language_code in utils.LANGUAGE_CODES else 'en'
        self.lang = getattr(utils.LANGUAGE_STRINGS, self.language_code)
    
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
