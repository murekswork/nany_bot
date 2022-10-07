from . import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
from keyboards import profile_keyboard, main_keyboard, send_ticket_keyboard
from controllers import get_user_profile, send_articles

from loader import user_data_cache
from config import admin_contact


@dp.message_handler(Text(equals='кеш'))
async def show_cache(message: types.Message):
    print(user_data_cache)


@dp.message_handler(Text(equals='Профиль'))
async def profile(message: types.Message):
    user_id = message.from_user.id
    user_profile = get_user_profile(user_id)
    text = f'ID: {user_id}\n' \
           f'Имя: {user_profile["name"]}\n' \
           f'Дата рождения: {user_profile["child_birthday"]}\n' \
           f'Подписка до: {user_profile["subscription_end"]}'
    await message.answer(text, reply_markup=profile_keyboard())


@dp.message_handler(Text(equals='Помочь советом'))
async def send_ticket_menu(message: types.Message):
    await message.answer('Отправить совет или назад', reply_markup=send_ticket_keyboard())


@dp.message_handler(Text(equals='Назад'))
async def go_back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_keyboard())


@dp.message_handler(Text(equals='Связь'))
async def contact_admin(message: types.Message):
    await message.answer(f'Для связи с администратором используйте этот контакт: {admin_contact}')


@dp.message_handler(Text(equals='сенд'))
async def main_algorithm(message: types.Message):
    await send_articles()
