import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config


class InitBot:
    bot = Bot(token=config.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    conn = sqlite3.connect('pet_helper.db')
    curs = conn.cursor()


init_bot = InitBot()
