from aiogram import types


from extentions import db
from misc import date_validator, datetime_to_str
from utils import calculate_subscription_end
from config import BASIC_SUBSCRIPTION_LENGTH
from loader import user_data_cache, bot
from models import create_article_model, create_user_model
from logger.loger import logger


def check_user_exist(user_id):
    if db.check_user_exist_db(user_id):
        return {'result': True, 'text': "Вы уже зарегистрированы"}
    else:
        return {'result': False}


def get_user_profile(user_id: int) -> dict:
    if user_id in user_data_cache:
        return user_data_cache[user_id]
    else:
        data = db.get_user_profile_db(user_id)
        user_data_cache[user_id] = data
        return data


def apply_for_registration(message: types.Message) -> (dict or bool):
    user_id = int(message.from_user.id)

    birthday = message.text
    birth_date_datetime = date_validator.validate(birthday)
    if not birth_date_datetime:
        return False

    subscription_end_date = calculate_subscription_end(BASIC_SUBSCRIPTION_LENGTH)
    birthday = datetime_to_str(birth_date_datetime)
    subscription_end = datetime_to_str(subscription_end_date)

    logger.debug(f'USER:{user_id} - REGISTERED')

    return {'user_id': user_id, 'birthday': birthday, 'subscription_end': subscription_end}


def register_new_user(message: types.Message) -> (dict or bool):
    """

    This function is responsible for user register

    :param message: aiogram.types.Message - basic user input
    :return: True, otherwise dict with success and text keys
    """

    handled_results = apply_for_registration(message)
    logger.debug(f'USER:{message.from_user.id}-START REGISTER')
    if not handled_results:
        return {'success': False, 'text': "Дата введена в неверном формате. "
                                          "Пожалуйста, введите дату в формате день.месяц.год (13.01.2022)"}

    success = db.register_new_user(**handled_results)

    if not success:
        print("SOMETHING WENT WRONG WHILE REGISTERING NEW USER")
        return {'success': False, 'text': "Юзер уже существует, идиот!"}
    # fix, error if return bool
    return {'success': True}


def change_profile_name_controller(new_name: types.Message, user_id: types.message) -> (dict or bool):
    print(new_name)
    if new_name != '' and new_name is not None:
        if db.change_profile_name_db(new_name, user_id) is True:
            logger.debug(f'USER:{user_id} - CHANGED NAME')
            return {'success': True}
    else:
        return {'success': False}


def change_birthday_controller(date: str, user_id: int) -> dict:
    correct_date = date_validator.validate(date)
    try:
        correct_date = datetime_to_str(correct_date)
    except TypeError:
        return {'success': False, 'text': 'Ошибка, укажите дату в формате дд.мм.гг (01.01.2021)'}

    date_changed = db.change_birthday_db(user_id, correct_date)
    if not date_changed:
        return {'success': False, 'text': 'Ошибка, повторите позднее'}
    user_data_cache[user_id]['child_birthday'] = correct_date
    logger.debug(f'USER:{user_id} - CHANGED BIRTHDAY')
    return {'success': True}


def send_advice_controller(user_id: int, message: str, ticket_date) -> (dict or bool):
    message_text = str(message)
    result = db.send_advice_db(user_id, message_text, ticket_date)
    if result['success'] is True:
        logger.debug(f'USER:{user_id} - SENT ADVICE')
        return {'success': True, 'ticket_id': result['ticket_id']}
    else:
        return {'success': False, 'text': 'Проблема с базой данных, повторите позднее'}


async def send_articles():
    user_model_list = create_user_model()
    article_model_list = create_article_model()
    for article in article_model_list:
        for user in user_model_list:
            if article.age == user.age and user.check_subscription() == 'ACTIVE':
                await send_article_to_user(user.id, article)
    logger.warning('SENT DAILY ARTICLES')

async def send_article_to_user(user_id, article):
    await bot.send_message(user_id, f'{article.topic}\n{article.url}')
