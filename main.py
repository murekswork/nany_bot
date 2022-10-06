def run_bot():
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run_bot()
