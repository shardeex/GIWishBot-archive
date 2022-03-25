from typing import *

from aiocache import Cache
from aiogram import types, BaseMiddleware, Router

from app.schema import Player


class PlayerCacheMiddleware(BaseMiddleware):

    ttl = 600  # player data time-to-live
    allowed_types = types.Message | types.CallbackQuery | types.InlineQuery
    allowed_observers = 'message', 'callback_query', 'inline_query'

    def __init__(self) -> None:
        self.__cache = Cache()
    
    def setup(
        self,
        router: Router,
    ):
        '''Register middleware for filtered events in router

        :param self:
        :param Router router:
        :return BaseMiddleware:
        '''
        for event_name, observer in router.observers.items():
            if event_name in self.allowed_observers:
                observer.middleware(self)
        return self

    async def __call__(
        self,
        handler: Callable[[allowed_types, Dict[str, Any]], Awaitable[Dict]],
        event: allowed_types,
        data: Dict[str, Any]
    ) -> Any:
        # get player from cache or load from database
        player: Player | None = await self.__cache.get(event.from_user.id)
        if not player:
            player = await Player(event.from_user.id).load()
        
        # set player or update ttl
        await self.__cache.set(event.from_user.id, player, ttl=self.ttl)
        data['player'] = player

        result = await handler(event, data)
        
        # save player if handler returns {'save_player': True}
        if result.get('save_player'):
            await player.save()
            await self.__cache.set(player.id, player, ttl=self.ttl)

        return result

player_cache_middleware = PlayerCacheMiddleware()
