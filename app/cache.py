from functools import wraps

from aiocache import Cache
from aiogram.types import Message, CallbackQuery, InlineQuery

from app.schema import Player


class PlayersCache():

    ttl = 360

    def __init__(self):
        self.__cache = Cache()

    async def load(self, player_id: int) -> Player:
        '''load
        '''
        player: Player | None = await self.__cache.get(player_id)
        if not player:
            player = await Player(player_id).load()

        # set user or update ttl
        await self.__cache.set(player_id, player, ttl=self.ttl)
        return player

    async def save(self, player: Player) -> None:
        '''save
        '''
        await player.save()
        await self.__cache.set(player.id, player, ttl=self.ttl)

class PlayerLoader:
    def __init__(self, user_id: int, with_save: bool):
        self.user_id = user_id
        self.with_save = with_save

    async def __aenter__(self):
        self.player = await players.load(self.user_id)
        return self.player
    
    async def __aexit__(self, exc_type, exc, tb):
        if self.with_save:
            await players.save(self.player)


def player_loader(with_save: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(event: Message|CallbackQuery|InlineQuery, *args, **kwargs):
            async with PlayerLoader(event.from_user.id, with_save) as p:
                await func(event, *args, player=p, **kwargs)
        return wrapper
    return decorator

players = PlayersCache()
