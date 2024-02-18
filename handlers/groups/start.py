from filters import IsGroup,CheckBadWords, ContainsHiddenLink,IsBotDelete,IsBotAdmin
from aiogram import types, html
from loader import dp,bot
from aiogram.filters import CommandStart,Command
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from keyboards.inline.buttons import add_group_button
import time,sqlite3,random
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



DATABASE_FILE = "bot.db"
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        username VARCHAR(50) NULL,
        title TEXT,
        group_id INTEGER,
        invite_link TEXT NULL,
        registration_date TEXT
    )
''')
conn.commit()


async def is_group_registered(group_id):
    cursor.execute('''
        SELECT group_id FROM groups WHERE group_id=?
    ''', (group_id,))
    result = cursor.fetchone()
    return result is not None


async def get_chat_owner(chat_id):
    try:
        admins = await bot.get_chat_administrators(chat_id)
        owner = next((admin for admin in admins if admin.status == 'creator'), None)
        return owner.user.id if owner else None
    except:
        pass
    return None

@dp.message(Command('stat'), IsGroup(), IsBotDelete())
async def stat_del(msg: types.Message):
    await msg.delete()

@dp.message(CommandStart(), IsGroup())
async def start_bot(message:types.Message):
    user = html.link(value=f"{message.from_user.full_name}", link=f"tg://user?id={message.from_user.id}")
    reaction_list = ["👍", "❤", "🔥", "🥰", "👏", "🎉", "🤩", "👌", "🕊", "😍", "❤‍🔥", "🌚", "⚡", "🏆", "👨‍💻", "👀", "😇", "🤝", "🤗", "🫡", "🗿", "🙉","😎"]
    await message.reply(f"Salom {user}",disable_web_page_preview=True)
    try:
        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
            is_big=False
        )
    except:
        pass


advertisers = []



async def has_restrict_permission(chat_id):
    try:
        bot_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        return bot_member.can_restrict_members
    except:
        return False
    
async def has_bot_permissions(chat_id):
    try:
        bot_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        return bot_member.can_invite_users
    except:
        return False
    
async def ads_delete(message):
    username = message.chat.username
    title = message.chat.title
    group_id = message.chat.id
    chat_type = message.chat.type.title()
    count_users = await bot.get_chat_member_count(chat_id=group_id)
    success = await has_bot_permissions(group_id)
    owner_id = await get_chat_owner(message.chat.id)
    if success:
        invite_link = await bot.export_chat_invite_link(chat_id=group_id)
    else:
        invite_link = None
    if not await is_group_registered(group_id):
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO groups (username,title,group_id,invite_link,registration_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, title, group_id, invite_link, registration_date))
        conn.commit()
        msg = f"""
{html.code(value=chat_type)}
<b>Name:</b> {title}
<b>Username:</b> {f"@{username}" if username else 'None'}
<b>{chat_type}🆔:</b> {html.code(value=group_id)}
<b>Reg 📆:</b> {registration_date}
<b>Members 👤:</b> {count_users}
"""
        await bot.send_message(chat_id=-1002039102176,text=msg,
        reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{chat_type}", url=invite_link if invite_link else 'https://t.me/ulugbekhusain'),
            ],
            [
                InlineKeyboardButton(text="Refresh",callback_data=f"refresh:{group_id}"),
                InlineKeyboardButton(text="Make Admin", callback_data=f'makeadmin:{group_id}'),
            ],
            [
                InlineKeyboardButton(text="Check New Admin", callback_data=f'checknewadmin:{group_id}')
            ],
            [
                InlineKeyboardButton(text="Leave Chat", callback_data=f'leavechat:{group_id}'),
                InlineKeyboardButton(text="Unban", callback_data=f'unban_me:{group_id}')
            ]
        ]

))
    if owner_id and owner_id != message.from_user.id:

        user = html.link(value=f"{message.from_user.full_name}", link=f"tg://user?id={message.from_user.id}")
        alert = f"❗️{user} <b>iltimos reklama tarqatmang!</b>"
        user_id = message.from_user.id
        if user_id in advertisers:
            restrict_permission = await has_restrict_permission(message.chat.id)
            if restrict_permission:
                try:
                    await message.delete()
                    await bot.restrict_chat_member(chat_id=message.chat.id,
                                                user_id=message.from_user.id,
                                                permissions=types.ChatPermissions(
                                                    can_send_messages=False,
                                                    can_send_media_messages=False,
                                                    can_send_polls=False,
                                                    can_send_other_messages=False,
                                                    can_add_web_page_previews=False,
                                                    can_change_info=False,
                                                    can_invite_users=False,
                                                    can_pin_messages=False,
                                                ),
                                                until_date=time.time() + 60)
                    await message.answer(f"{alert}\n{html.blockquote(value='👮🏻‍♂️ siz guruhdan vaqtinchaga <b>bloklandingiz</b>')}",reply_markup=add_group_button,disable_web_page_preview=True)
                except:
                    try:
                        await message.delete()
                    except:
                        pass
            else:
                try:
                    await message.delete()
                    await message.answer(alert,reply_markup=add_group_button,disable_web_page_preview=True)
                except:
                    pass
        else:
            try:
                await message.delete()
                await message.answer(alert,reply_markup=add_group_button,disable_web_page_preview=True)
                advertisers.append(user_id)
            except:
                pass
    elif owner_id and owner_id == message.from_user.id:
        pass     
    else:
        user = html.link(value=f"{message.from_user.full_name}", link=f"tg://user?id={message.from_user.id}")
        alert = f"❗️{user} <b>iltimos reklama tarqatmang!</b>"
        user_id = message.from_user.id
        if user_id in advertisers:
            restrict_permission = await has_restrict_permission(message.chat.id)
            if restrict_permission:
                try:
                    await message.delete()
                    await bot.restrict_chat_member(chat_id=message.chat.id,
                                                user_id=message.from_user.id,
                                                permissions=types.ChatPermissions(
                                                    can_send_messages=False,
                                                    can_send_media_messages=False,
                                                    can_send_polls=False,
                                                    can_send_other_messages=False,
                                                    can_add_web_page_previews=False,
                                                    can_change_info=False,
                                                    can_invite_users=False,
                                                    can_pin_messages=False,
                                                ),
                                                until_date=time.time() + 60)
                    await message.answer(f"{alert}\n{html.blockquote(value='👮🏻‍♂️ siz guruhdan vaqtinchaga <b>bloklandingiz</b>')}",reply_markup=add_group_button,disable_web_page_preview=True)
                except:
                    try:
                        await message.delete()
                    except:
                        pass
            else:
                try:
                    await message.delete()
                    await message.answer(alert,reply_markup=add_group_button,disable_web_page_preview=True)
                except:
                    pass
        else:
            try:
                await message.delete()
                await message.answer(alert,reply_markup=add_group_button,disable_web_page_preview=True)
                advertisers.append(user_id)
            except:
                pass


@dp.message(IsGroup(), CheckBadWords(), IsBotDelete())
async def bad_words(message: types.Message):
    await ads_delete(message=message)
@dp.edited_message(CheckBadWords(),IsGroup())
async def edited_bad_words(message: types.Message):
    await ads_delete(message=message)

@dp.message(ContainsHiddenLink(),IsGroup(), IsBotDelete())
async def handle_hidden_link(message: types.Message):
    await ads_delete(message=message)
@dp.edited_message(ContainsHiddenLink(), IsGroup())
async def edited_handle_hidden_link(message: types.Message):
    await ads_delete(message=message)
    

# botni ruxsati bo'lmaganda
    

# async def has_bot_permissions(chat_id):
#     try:
#         bot_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
#         return bot_member.can_invite_users
#     except:
#         return False



async def admin_note(message):
    group_id = message.chat.id
    owner_id = await get_chat_owner(group_id)
    if owner_id:
        owner = html.link(value=".", link=f"tg://user?id={owner_id}")
        user = html.link(value=f"{message.from_user.full_name}", link=f"tg://user?id={message.from_user.id}")
        reklama = html.link(value=f"Guruhda reklama tarqatildi!", link=f'https://t.me/c/{str(group_id)[4:]}/{message.message_id}')

        # success = await has_bot_permissions(group_id)
        # if success:
        #     invite_link = await bot.export_chat_invite_link(chat_id=group_id)
        # else:
        #     invite_link = None

        if message.from_user.id != owner_id:
            reaction_list = ["😴", "😭", "🤓", "👻","🥱","🥴","😡","🤮","😢","🤨","😐",]
            try:
                await message.reply(f"""❗️{user} <b>iltimos reklama tarqatmang!</b> {html.blockquote(value="Botda reklamalarni o'chirishi uchun ruxsat yo'q iltimos ruxsatlarni qayta sozlang")}{owner}""")
                await bot.set_message_reaction(
                    chat_id=group_id,
                    message_id=message.message_id,
                    reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
                    is_big=False
                )
            except:
                pass
            try:
                await bot.send_message(owner_id, f"❗ <b>{reklama}</b>\n\n" +
                                    f"👤 Foydalanuvchi: {user}\n" +
                                    f'🆔 User ID: {message.from_user.id}\n\n'+
                                    f'''{html.blockquote(value="Botda xabarlarni o'chirishi uchun ruxsat yo'q iltimos ruxsatlarni qayta sozlang")}''',protect_content=True)
            except:
                pass
        elif message.from_user.id == owner_id:
            reaction_list = ["😴", "😭", "🤓", "👻","🥱","🥴","😢","🤨","😐","🤷‍♂","🗿"]
            try:
                await message.reply(f"{user} Botda reklamalarni o'chirishi uchun ruxsat yo'q iltimos ruxsatlarni qayta sozlang")
                await bot.set_message_reaction(
                    chat_id=group_id,
                    message_id=message.message_id,
                    reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
                    is_big=False
                )
            except:
                pass
    else:
        reaction_list = ["😴", "😭", "🤓", "👻","🥱","🥴","😢","🤨","😐",]
        try:
            await message.reply(f"❗️ <b>Iltimos reklama tarqatmang!</b> Botda xabarlarni o'chirishi uchun ruxsat yo'q iltimos ruxsatlarni qayta sozlang")
            await bot.set_message_reaction(
                chat_id=group_id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
                is_big=False
            )
        except:
            pass

# refresh invite link


# @dp.callback_query(lambda query: query.data.startswith("invitelink:"))
# async def refresh_invite_link(callback_query: types.CallbackQuery):
#     try:
#         _, group_id = callback_query.data.split(":")
#         group_id = int(group_id)
#         get_chat = await bot.get_chat(group_id)
#         title = get_chat.title
#         success = await has_bot_permissions(group_id)
#         if success:
#             invite_link = await bot.export_chat_invite_link(chat_id=group_id)
#             await callback_query.answer(f"Link yangilandi", show_alert=True)
#         else:
#             invite_link = None
#             await callback_query.answer(f"Botni ruxsati yo'q ruxsatlarni qayta sozlang", show_alert=True)

#         await bot.edit_message_text(chat_id=callback_query.message.chat.id,
#                                     message_id=callback_query.message.message_id,
#                                     text=f"❗ <b>Guruhda reklama tarqatildi!</b>\n\n" +
#                                     f"👤 Guruh: {title}\n\n" +
#                                     f"Botda xabarlarni o'chirishi uchun ruxsat yo'q iltimos ruxsatlarni qayta sozlang",reply_markup=InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(text="Yangi Link", url=invite_link if invite_link else 'https://t.me/channelnot_found'),
#                     InlineKeyboardButton(text="Refresh Link",callback_data=f"invitelink:{group_id}"),
#                 ]
#                 ]
#                 ))
#     except:
#         pass


@dp.message(IsBotAdmin(),IsGroup(), ~IsBotDelete(), CheckBadWords())
async def admin_note_badword(message: types.Message):
    await admin_note(message)

@dp.message(IsBotAdmin(),IsGroup(), ~IsBotDelete(), ContainsHiddenLink())
async def admin_note_hidlink(message: types.Message):
    await admin_note(message)


