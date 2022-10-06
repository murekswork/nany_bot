
from logger.loger import logger


def run_bot():
    from aiogram import executor
    from handlers import dp
    logger.debug('Bot started')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run_bot()
