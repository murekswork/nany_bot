# from . import dp
# from loader import bot
# from aiogram.dispatcher.filters import Text
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from FSM.birthday_FSM import FSMInputDate
# from controllers import change_profile_name_controller, change_birthday_controller
# from misc.basic_responses import CHANGE_NAME
# from keyboards import main_keyboard
#
# from loader import user_data_cache
#
#
# @dp.message_handler(Text(equals='Изменить имя'))
# async def change_profile_name(message: types.Message):
#     await message.answer(CHANGE_NAME)
#     await FSMInputDate.name.set()
#
#
# @dp.message_handler(state=FSMInputDate.name)
# async def change_name(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     result = change_profile_name_controller(message.text, user_id)
#
#     if result['success'] is True:
#         user_data_cache[user_id]['name'] = message.text
#         await state.finish()
#         await message.answer(f"Имя успешно изменено на: {message.text}", reply_markup=main_keyboard())
#
#
# @dp.message_handler(Text(equals='Изменить дату рождения'))
# async def change_birthday(message: types.Message):
#     await message.answer("Введите новую дату: ")
#     await FSMInputDate.change_date.set()
#
#
# @dp.message_handler(state=FSMInputDate.change_date)
# async def change_birthday(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     result = change_birthday_controller(message.text, user_id)
#     await state.finish()
#     if result['success']:
#         await message.answer(f'Дата рождения ребёнка изменено на: {message.text}', reply_markup=main_keyboard())
#     else:
#         await message.answer(result['text'], reply_markup=main_keyboard())
#         return result['text']
#
# @dp.message_handler(Text(equals='Назад'))
# async def go_back(message: types.Message):
#     await message.answer("Главное меню", reply_markup=main_keyboard())
#
#
# @dp.message_handler(Text(equals='Помочь советом'))
# async def help_with_advice(message: types.Message):
#     user_id = message.from_user.id
#     await message.answer('Напишите ваше предложение и мы обязательно его рассмотрим')