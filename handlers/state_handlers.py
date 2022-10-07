import datetime

from . import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from FSM.birthday_FSM import FSMInputDate
from controllers import change_profile_name_controller, change_birthday_controller, send_advice_controller
from misc.basic_responses import CHANGE_NAME
from keyboards import main_keyboard

from loader import user_data_cache


@dp.message_handler(Text(equals='Изменить имя'))
async def change_profile_name(message: types.Message):
    await message.answer(CHANGE_NAME)
    await FSMInputDate.name.set()


@dp.message_handler(state=FSMInputDate.name)
async def change_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    result = change_profile_name_controller(message.text, user_id)

    if result['success'] is True:
        user_data_cache[user_id]['name'] = message.text
        await state.finish()
        await message.answer(f"Имя успешно изменено на: {message.text}", reply_markup=main_keyboard())


@dp.message_handler(Text(equals='Изменить дату рождения'))
async def change_birthday(message: types.Message):
    await message.answer("Введите новую дату: ")
    await FSMInputDate.change_date.set()


@dp.message_handler(state=FSMInputDate.change_date)
async def change_birthday(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    result = change_birthday_controller(message.text, user_id)
    await state.finish()
    if result['success']:
        await message.answer(f'Дата рождения ребёнка изменено на: {message.text}', reply_markup=main_keyboard())
    else:
        await message.answer(result['text'], reply_markup=main_keyboard())
        return result['text']


@dp.message_handler(Text(equals='Отправить совет'))
async def send_advice(message: types.Message):
    await message.answer('Напишите ваше предложение и мы обязательно его рассмотрим')
    await FSMInputDate.ticket_state.set()

@dp.message_handler(state=FSMInputDate.ticket_state)
async def send_advice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    controller = send_advice_controller(user_id, message.text, datetime.datetime.today().strftime('%d.%m:%H:%M'))
    await state.finish()
    if controller['success']:
        await message.answer(f'Ваше обращение под номером #{controller["ticket_id"]} получено.\n'
                             f'После обработки обязательно свяжемся с вами.', reply_markup=main_keyboard())
    else:
        await message.answer(controller['text'], reply_markup=main_keyboard())
        return controller['text']


