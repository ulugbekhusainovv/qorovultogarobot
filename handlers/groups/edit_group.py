# from aiogram import types,F
# from filters import IsGroup,IsGroupAdmin
# from loader import dp,bot
# import asyncio
# from aiogram.filters import Command
# import io
# @dp.message(IsGroup(), IsGroupAdmin(),Command('set_title'))
# async def set_name(message: types.Message):
#     replied = message.reply_to_message
#     if replied:
#         try:
#             text = replied.text
#             await message.chat.set_title(title=text)
#             await message.delete()
#             await replied.delete()
#         except: pass
#     else:
#         error = await message.reply(text="Guruh nomini o'zgartirish uchun habarga reply qiling")
#         await asyncio.sleep(5)
#         await error.delete()

# @dp.message(IsGroup(), IsGroupAdmin(),Command('set_description'))
# async def set_des(message: types.Message):
#     try:
#         replied = message.reply_to_message
#         text = replied.text
#         await message.chat.set_description(description=text)
#         await message.delete()
#         await replied.delete()
#     except: 
#         pass
    
# @dp.message(IsGroup(), IsGroupAdmin(),Command('set_photo'))
# async def set_image(message: types.Message):
#     try:
#         replied = message.reply_to_message
#         file_id = replied.photo[-1].file_id
#         file = await bot.get_file(file_id=file_id)
#         bytes = io.BytesIO()
#         await bot.download(file=file, destination=bytes)
#         photo = types.input_file.BufferedInputFile(file=bytes.read(), filename="group_image.jpg")
#         await message.chat.set_photo(photo=photo)
#     except:
#         error =  await message.reply(text="Xatolik yuz berdi iltimos qaytadan urinib ko'ring")
#         await asyncio.sleep(3)
#         await error.delete()
#     await message.delete()
#     await replied.delete()