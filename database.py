import sqlite3
from logger.loger import logger


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('afkposakfpaskf.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # dev_command = 'DROP TABLE users'
        # self.cursor.execute(dev_command)
        # self.connection.commit()
        command = "CREATE TABLE IF NOT EXISTS users (tg_id integer PRIMARY KEY NOT NULL, " \
                  "child_birthday text, " \
                  "subscription_end text," \
                  "name text DEFAULT NONE);"

        self.cursor.execute(command)
        self.connection.commit()

    def get_articles(self):
        command = f"SELECT * FROM article"
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def get_users_list_db(self):
        """
        This function returns dict with users id and users birthday
        :return:
        """
        command = f'SELECT tg_id, child_birthday, subscription_end FROM users'
        self.cursor.execute(command)
        user_list = self.cursor.fetchall()
        return user_list

    def register_new_user(self, user_id, birthday, subscription_end):

        try:
            command = "INSERT INTO users(tg_id, child_birthday, subscription_end ) VALUES (?, ?, ?);"

            self.cursor.execute(command, (user_id, birthday, subscription_end))
            self.connection.commit()
            logger.debug(f'USER:{user_id} - REGISTERED IN DATABASE')
        except sqlite3.IntegrityError:
            logger.warning(f'USER:{user_id} - ERROR REGISTERING DB', exc_info=True)
            return False

        return self.connection.total_changes

    def check_user_exist_db(self, user_id: int) -> bool:
        command = f"SELECT * FROM users WHERE tg_id = ?"
        self.cursor.execute(command, (user_id,))
        result = self.cursor.fetchone()
        if not result:
            return False
        else:
            return True

    def get_user_profile_db(self, user_id: int):
        command = f"SELECT child_birthday, subscription_end, name FROM users WHERE tg_id = ?"
        self.cursor.execute(command, (user_id,))
        result = self.cursor.fetchone()
        print(result)
        return {'child_birthday': result[0], 'subscription_end': result[1], 'name': result[2]}

    def change_profile_name_db(self, new_name: str, user_id: int):
        try:
            command = f"UPDATE users SET name = ? WHERE tg_id = ?"
            self.cursor.execute(command, (str(new_name), user_id))
            self.connection.commit()
            logger.debug(f'USER:{user_id} - CHANGED NAME DATABASE')
            return True
        except:
            logger.warning(f'USER:{user_id} - ERROR CHANGE NAME DATABASE', exc_info=True)

    def change_birthday_db(self, user_id: int, new_date: str):
        try:
            command = f"UPDATE users SET child_birthday = ? WHERE tg_id = ?"
            self.cursor.execute(command, (new_date, user_id))
            self.connection.commit()
            print(f'Birthday changed in database! to {new_date}')
            logger.debug(f'USER:{user_id} - CHANGED BIRTHDAY DATABASE')
            return True
        except:
            logger.warning(f'USER:{user_id} - ERROR CHANGE NAME DATABASE', exc_info=True)

    def send_advice_db(self, user_id: int, message: str, ticket_date: str) -> dict:
        try:
            command_create_table = "CREATE TABLE IF NOT EXISTS " \
                                   "tickets" \
                                   "(ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                                   "tg_id INTEGER, " \
                                   "ticket_text TEXT, " \
                                   "date TEXT)"
            self.cursor.execute(command_create_table)
            self.connection.commit()
            command = "INSERT INTO tickets(tg_id, ticket_text, date) VALUES (?, ?, ?)"
            self.cursor.execute(command, (user_id, message, ticket_date))
            self.connection.commit()
            print('New advice ticket added in database!')
            self.cursor.execute(f'SELECT ticket_id FROM tickets WHERE tg_id = "{user_id}" AND date = "{ticket_date}"')
            logger.debug(f'USER:{user_id} - SEND ADVICE DATABASE')
            return {'success': True, 'ticket_id': self.cursor.fetchone()[0]}
        except:
            logger.warning(f'USER:{user_id} - ERROR SEND ADVICE DATABASE', exc_info=True)
            return {'success': False}




