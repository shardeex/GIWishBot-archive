from __future__ import annotations

from datetime import datetime

import sqlalchemy

import database as db


class Player:
    id: int

    showcase: list[dict[str, str]] = db.players.showcase_default
    inventory: dict[str, int] = db.players.invnetory_default
    pities: dict[str, dict[str, bool | int | None]] = db.players.pities_default

    blessing_of_the_welkin_moon: bool = False
    last_wish: datetime = datetime.min
    moon_last_wish: datetime = datetime.min

    masterless_stardust: int = 0
    masterless_starglitter: int = 0
    genesis_crystals: int = 0

    lock: bool = False  # throttling

    def __init__(self, user_id: int) -> None:
        self.id = user_id
        self.__database_keys = [c.name for c in db.players.table.columns]
    
    async def create(self) -> None:
        '''creates user data in database

        '''
        # init only 'id', others are default
        query = db.players.table.insert().values(id=self.id)
        await db.database.execute(query=query)
    
    async def load(self, create=True) -> Player:
        '''loads user data from database

        create: bool — if True, creates profile if not loaded
        '''
        columns = [getattr(db.players.table.c, i) for i in self.__database_keys]

        query = sqlalchemy.select(*columns
        ).where(db.players.table.c.id == self.id)

        result = await db.database.fetch_one(query=query)

        if not result:
            if create:
                await self.create()  # empty user
            else:
                raise ValueError('non-existent id')
        else:
            [setattr(self, i, result[i]) for i in self.__database_keys]
        return self
    
    async def save(self) -> Player:
        '''saves user data to database
        '''
        values = dict([(i, getattr(self, i)) for i in self.__database_keys])

        query = sqlalchemy.update(db.players.table
        ).values(**values
        ).where(db.players.table.c.id == self.id)

        await db.database.execute(query)
        return self
