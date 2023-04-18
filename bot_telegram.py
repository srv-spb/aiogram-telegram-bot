from aiogram import Bot, types
# используется для улавливания событий происходящих в Telegram и связанных
# с ботом (в чате, в который добавлен бот, непосредственно в диалоге с ботом)
from aiogram.dispatcher import Dispatcher
# утилита для запуска работы бота
from aiogram.utils import executor

import os

# существует 2 режима работы бота:
# LongPolling - программа с ботом сама опрашивает сервер Telegram об имеющихся событиях
# на которые может реагировать бот. Основной минус - если сеть отвалится то программа вылетает
# и надо перезапускать
# WebHook - должен быть создан сервер на который будут приходить запросы от сервера Telegram
# в соответствии с соответствующим API


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler()
async def echo_send(message: types.Message):
    # await message.answer(message.text)
    # await message.reply(message.text)
    # бот отправляет сообщение в ЛС пользователя, но только если пользователь активировал этого бота
    # иначе вылетит исключение
    await bot.send_message(message.from_user.id, message.text)


# skip_updates - паараметр для игнорирования запросов поступивших боту, когда он был офлайн
executor.start_polling(dp, skip_updates=True)
