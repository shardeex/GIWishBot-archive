from aiogram import types

from loader import i18n
from modules import help


_ = i18n.gettext

async def cmd(message: types.Message) -> None:
    """/help command

    Args:
        message (types.Message): message object
    """
    print(message.from_user.language_code)
    text = help.message.get()
    await message.answer(str(text))
