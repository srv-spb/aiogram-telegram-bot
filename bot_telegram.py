import string

from aiogram import Bot, types
# используется для улавливания событий происходящих в Telegram и связанных
# с ботом (в чате, в который добавлен бот, непосредственно в диалоге с ботом)
from aiogram.dispatcher import Dispatcher
# утилита для запуска работы бота
from aiogram.utils import executor

import os, json

# существует 2 режима работы бота:
# LongPolling - программа с ботом сама опрашивает сервер Telegram об имеющихся событиях
# на которые может реагировать бот. Основной минус - если сеть отвалится то программа вылетает
# и надо перезапускать
# WebHook - должен быть создан сервер на который будут приходить запросы от сервера Telegram
# в соответствии с соответствующим API


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

'''*********************КЛИЕНТСКАЯ ЧАСТЬ*********************'''


async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/PizzaAssistantBot')


@dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


@dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная д. 15')


'''*********************АДМИНСКАЯ ЧАСТЬ**********************'''

'''*********************ОБЩАЯ ЧАСТЬ**************************'''


@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()
    else:
        await message.reply(message.text)
    # await message.answer(message.text)
    # await message.reply(message.text)
    # бот отправляет сообщение в ЛС пользователя, но только если пользователь активировал этого бота
    # иначе вылетит исключение
    # await bot.send_message(message.from_user.id, message.text)


# skip_updates - параметр для игнорирования запросов поступивших боту, когда он был офлайн
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
