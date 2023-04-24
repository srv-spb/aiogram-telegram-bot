from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot
from keyboards import kb_client
from database import sqlite_bd


# строка ниже уже не нужна для регистрации функции в качестве обработчика сообщений
# т.к. определение функции находится не в одном файле с командой запуска бота
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/PizzaAssistantBot')


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


# добавлено свойство, которое определяет, что необходимо удалить клавитатуру после отправки сообщения
# восстановить можно отправив /start
# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная д. 15', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands='[Меню]')
async def pizza_menu_command(message: types.Message):
    await sqlite_bd.sql_read_all(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
