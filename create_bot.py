import os

from aiogram import Bot
# используется для улавливания событий происходящих в Telegram и связанных
# с ботом (в чате, в который добавлен бот, непосредственно в диалоге с ботом)
from aiogram.dispatcher import Dispatcher


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
