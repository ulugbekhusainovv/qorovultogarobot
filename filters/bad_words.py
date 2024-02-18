BAD_WORDS=['http', 'https', 'www','.com','@',"t.me",'lichka','bioda','profil','профиль','био',"18+", "porn", "seks",'sexs',"порно","секс","+998","+996","aksiya","chegirma","taklif","bepul","reklama",'sotuvda']
# BAD_WORDS = ['https']

from aiogram.filters import BaseFilter
from aiogram import types

# class CheckBadWords(BaseFilter):
    
#     async def __call__(self, message: types.Message) -> bool:
#         if message.text and isinstance(message.text, str):
#             lower_text = message.text.lower()
#             for word in BAD_WORDS:
#                 if word in lower_text:
#                     return True
#             return False

# class CheckBadWords(BaseFilter):
#     async def __call__(self, message: types.Message) -> bool:
#         if (message.text and isinstance(message.text, str) and
#                 any(word in message.text.lower() for word in BAD_WORDS)):
#             return True

#         if (message.caption and isinstance(message.caption, str) and
#                 any(word in message.caption.lower() for word in BAD_WORDS)):
#             return True

#         return False or self.is_edited(message)

#     def is_edited(self, message: types.Message) -> bool:
#         return message.edit_date is not None
# class CheckBadWords(BaseFilter):
#     async def __call__(self, message: types.Message) -> bool:
#         if self.is_edited(message):
#             return self.check_content(message.text)

#         if message.text:
#             return self.check_content(message.text)

#         if message.caption:
#             return self.check_content(message.caption)

#         return False

#     def check_content(self, text: str) -> bool:
#         return any(word in text.lower() for word in BAD_WORDS)

#     def is_edited(self, message: types.Message) -> bool:
#         return message.edit_date is not None

class CheckBadWords(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if self.is_edited(message):
            return self.check_for_bad_words(message.text.lower())

        if (message.text and isinstance(message.text, str) and
                self.check_for_bad_words(message.text.lower())):
            return True

        if (message.caption and isinstance(message.caption, str) and
                self.check_for_bad_words(message.caption.lower())):
            return True

        return False

    def is_edited(self, message) -> bool:
        return message.edit_date is not None

    def check_for_bad_words(self, text: str) -> bool:
        return any(word in text for word in BAD_WORDS)
