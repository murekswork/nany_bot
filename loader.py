from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import extentions
from config import MAIN_TOKEN

bot = Bot(token=MAIN_TOKEN)
storage = MemoryStorage()

user_data_cache = {}

dp = Dispatcher(bot, storage=storage)
db = extentions.db
