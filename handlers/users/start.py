from aiogram.filters import CommandStart,CommandObject
from loader import dp,bot
from aiogram import types,html
from keyboards.inline.buttons import add_group_button
from filters import IsPrivate
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from data.config import BOT
from datetime import datetime
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
import random
from keyboards.inline.buttons import programmer

# text = '''
# Assalamu alaykum Men <b>Qorovul Botman</b> Meni guruhingizga qo'shing va <b>reklamalardan</b> halos bo'ling.
# '''


silka = html.link(value="silkalarni",link=f"https://t.me/{BOT}?start=true")

text=f'''
Salom👋
<b>Men reklamalarni, yashirin {silka} Guruhlarda o'chirib beraman 👨🏻‍✈️</b>

{html.blockquote(value="<b>Guruhdagi kirdi - chiqdi 🔞+ xabarlarini va hatto tahrirlangan xabarlarni tekshiraman va u reklama boʻlsa oʻchiraman 🤖</b>")}

Men ishlashim uchun Guruhingizga <b>ADMIN</b> qilishingiz kerak😎
'''

help_text = """Sizga qanday yordam kerak"""


DATABASE_FILE = "bot.db"
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR(30) NULL,
        full_name TEXT,
        telegram_id INTEGER,
        registration_date TEXT
    )
''')
conn.commit()


async def is_user_registered(telegram_id):
    cursor.execute('''
        SELECT telegram_id FROM users WHERE telegram_id=?
    ''', (telegram_id,))
    result = cursor.fetchone()
    return result is not None


@dp.message(CommandStart(),IsPrivate())
async def handle_start(message: types.Message, command: CommandObject):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    is_premium = message.from_user.is_premium
    is_bot = message.from_user.is_bot
    username = message.from_user.username
    args = command.args


    if args == 'help':
        reaction_list = ["🫡",'🧑🏻‍💻','✊','👍🏻','👌']
        try:
            await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
            is_big=False
        )
        except: 
            pass
        await message.reply(help_text, reply_markup=programmer)
    else:

        reaction_list = ["👍", "❤", "🔥", "🥰", "👏", "🎉", "🤩", "👌", "🕊", "😍", "❤‍🔥", "⚡", "🏆", "👨‍💻", "👀", "😇", "🤝", "🤗", "🫡", "🗿", "🙉","😎",]
        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
            is_big=False
        )

        if not await is_user_registered(telegram_id):
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO users (username,full_name,telegram_id,registration_date)
                VALUES (?, ?, ?, ?)
            ''', (username,full_name, telegram_id, registration_date))
            conn.commit()
            await message.answer(text=text, reply_markup=add_group_button,disable_web_page_preview=True)
            await bot.send_message(chat_id=-1002039102176,text=f"New 👤: {full_name}\nUsername📩: {html.code(value=username)}\nTelegram 🆔: {html.code(value=telegram_id)}\nReg 📆: {registration_date}\nIs 🤖: {is_bot}\nPremium🤑: {is_premium}",reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Profile", url=f"tg://user?id={telegram_id}")
                ]
            ]
    ))
        else:
            await message.reply(text=text, reply_markup=add_group_button,disable_web_page_preview=True)

