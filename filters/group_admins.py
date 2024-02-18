from aiogram.filters import BaseFilter
from aiogram import types
from loader import bot
from aiogram.enums import ChatMemberStatus


class IsGroupAdmin(BaseFilter):
    
    async def __call__(self, message: types.Message) -> bool:
        user = await bot.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
        # return user.status.CREATOR
        return user.status.status == 'creator'


# from aiogram.types import ChatMemberStatus

# class IsGroupAdmin(BaseFilter):
    
#     async def __call__(self, message: types.Message) -> bool:
#         return await self.is_admin(message.chat.id, message.from_user.id)

#     async def is_admin(self, chat_id, user_id) -> bool:
#         try:
#             chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
#             return chat_member.status == ChatMemberStatus.CREATOR
#         except Exception as e:
#             print(f"Xatolik yuz berdi: {e}")
#             return False