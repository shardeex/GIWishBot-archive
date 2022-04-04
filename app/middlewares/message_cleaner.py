import asyncio
from typing import *

from aiogram import types, BaseMiddleware, Router
from aiogram.exceptions import TelegramBadRequest

from app.loader import bot


class MessageCleaner(BaseMiddleware):

    allowed_types = types.Message | types.CallbackQuery | types.InlineQuery
    allowed_observers = 'message', 'callback_query', 'inline_query'
    
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
                observer.outer_middleware(self)
        return self

    async def __call__(
        self,
        handler: Callable[[allowed_types, dict[str, Any]], Awaitable[dict]],
        event: allowed_types,
        data: Dict[str, Any]
    ) -> Any:
        result = await handler(event, data)

        # {'clean_messages': [{'message': <aiogram.types.Message>, 'delay': <int>}, ...]}
        if isinstance(result, dict):
            if (messages_data := result.get('clean_messages')):
                for data in messages_data:
                    message = cast(types.Message, data['message'])
                    delay = cast(int, data['delay'])
                    asyncio.create_task(self.delete_after(message, delay))

        return result
    
    async def delete_after(self, message: types.Message, delay) -> None:
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except TelegramBadRequest:  # no admin rights in chat
            pass


message_cleaner_middleware = MessageCleaner()
