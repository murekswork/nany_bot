from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from FSM import FSMInputDate

from . import dp
from keyboards import initial_keyboard, main_keyboard, profile_keyboard
from misc import basic_responses
from controllers import register_new_user, check_user_exist


@dp.message_handler(commands='start')
async def start(message: types.Message):
    user_exist = check_user_exist(message.from_user.id)
    if user_exist['result'] is True:
        await message.answer(user_exist['text'], reply_markup=main_keyboard())
    else:
        await message.answer('Привет! Я постараюсь помочь тебе в уходе за малышом и в его воспитании!\nДля'
                             ' начала нужно указать возраст малыша, для этого нажми кнопку 👶Указать возраст',
                             reply_markup=initial_keyboard())


@dp.message_handler(Text(equals='👶Указать возраст'))
async def set_child_birthday(message: types.Message):
    user_exist = check_user_exist(message.from_user.id)
    if user_exist['result'] is True:
        await message.answer('Вы уже зарегистрированы', reply_markup=main_keyboard())
    else:
        await message.answer(basic_responses.SET_BIRTHDAY)
        await message.answer('Введите дату:', reply_markup=None)
        await FSMInputDate.date.set()


@dp.message_handler(state=FSMInputDate.date)
async def state1(message: types.Message, state: FSMContext):

        result = register_new_user(message)
        if not result['success']:
            await message.answer(result['text'])
        else:
            await message.answer(basic_responses.REGISTRATION_SUCCESSFULL, reply_markup=main_keyboard())
            await state.finish()
