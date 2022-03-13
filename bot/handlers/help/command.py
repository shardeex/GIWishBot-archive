from aiogram import types

import i18n


async def cmd(message: types.Message) -> None:
    """/help command

    Args:
        message (types.Message): message object
    """
    text = i18n.get('help:message', message.from_user.language_code)
    await message.answer(text)
