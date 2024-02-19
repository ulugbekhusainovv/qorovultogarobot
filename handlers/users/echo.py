from loader import dp,bot
from filters import IsPrivate
from aiogram import types,html,F
from data.config import BOT
from keyboards.inline.buttons import add_group_button
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
import random

silka = html.link(value="silkalarni",link=f"https://t.me/{BOT}?start=true")

text=f'''
Salom👋
<b>Men reklamalarni, yashirin {silka} Guruhlarda o'chirib beraman 👨🏻‍✈️</b>

{html.blockquote(value="<b>Guruhdagi kirdi - chiqdi 🔞+ xabarlarini va hatto tahrirlangan xabarlarni tekshiraman va u reklama boʻlsa oʻchiraman 🤖</b>")}

Men ishlashim uchun Guruhingizga <b>ADMIN</b> qilishingiz kerak😎
'''



@dp.message(IsPrivate(), F.text)
async def echo_bot(message:types.Message):
    # try:
    #     reaction_list = ["👍", "❤", "🔥", "🥰", "👏", "🎉", "🤩", "👌", "🕊", "😍", "❤‍🔥", "⚡", "🏆", "👨‍💻", "👀", "😇", "🤝", "🤗", "🫡", "🗿", "🙉","😎",]
    #     await bot.set_message_reaction(
    #         chat_id=message.chat.id,
    #         message_id=message.message_id,
    #         reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
    #         is_big=False
    #     )
    # except:
    #     pass
    print("salom")
    await message.reply(text=text, reply_markup=add_group_button,disable_web_page_preview=True)
