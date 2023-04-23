import os

from aiogram import Bot
# используется для улавливания событий происходящих в Telegram и связанных
# с ботом (в чате, в который добавлен бот, непосредственно в диалоге с ботом)
from aiogram.dispatcher import Dispatcher
# для хранения данных в оперативной памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
