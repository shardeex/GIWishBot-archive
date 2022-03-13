from aiogram import types
from aiogram.dispatcher.filters import BaseFilter


class PrivateChat(BaseFilter):

    async def __call__(self, _: types.Message, event_chat: types.Chat) -> bool:
        if event_chat:
            return event_chat.type == 'private'
        else:
            return False
