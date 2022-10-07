from extentions import db
import datetime

from logger.loger import logger


class Article:

    def __init__(self, id, topic, url, age):
        self.id = id
        self.topic = topic
        self.url = url
        self.age = age


class User:

    def __init__(self, id, birthday, subscription):
        self.id = id
        self.age = self.get_date_subtract(birthday)
        self.check_subscription = self.check_subscription(subscription)

    @staticmethod
    def get_date_subtract(birth_date):
        dateformat = '%d.%m.%Y'
        birth_date = datetime.datetime.strptime(birth_date, dateformat).date()
        today = datetime.datetime.today().date()
        delta = (today - birth_date).days
        return delta

    @staticmethod
    def check_subscription(subscription):
        dateformat = '%d.%m.%Y'
        subscription_date = datetime.datetime.strptime(subscription, dateformat)
        if subscription_date > datetime.datetime.today():
            return 'ACTIVE'
        else:
            return 'EXPIRED'

def create_article_model():

    all_articles = db.get_articles()
    article_models = []
    for article in all_articles:
        article_models.append(Article(
            id=article[0],
            topic=article[1],
            url=article[2],
            age=article[3]
        ))
    return article_models


def create_user_model():

    all_users = db.get_users_list_db()
    user_models = []
    for user in all_users:
        user_models.append(User(
            id=user[0],
            birthday=user[1],
            subscription=user[2]
        ))
    return user_models
