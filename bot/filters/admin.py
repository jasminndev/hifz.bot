from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.database import conf


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in conf.bot.ADMIN_IDS
