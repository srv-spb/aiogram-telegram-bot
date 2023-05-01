from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
answers = dict()


# Для запуска бота поменять в bot_run.bat имя, запускаемого python-файла
# кнопка ссылка
# по кнопке в ряд
url_kb = InlineKeyboardMarkup(row_width=2)
url_button1 = InlineKeyboardButton(text='Ссылка1', url='https://www.youtube.com')
url_button2 = InlineKeyboardButton(text='Ссылка2', url='https://www.google.com')
buttons_array = [InlineKeyboardButton(text='Ссылка3', url='https://www.google.com'),
                 InlineKeyboardButton(text='Ссылка4', url='https://www.google.com'),
                 InlineKeyboardButton(text='Ссылка5', url='https://www.google.com')]
# url_kb.add(url_button1, url_button2)
# row_width не влияет на расположение кнопок добавленных при помощи метода row
# url_kb.add(url_button1, url_button2).row(*buttons_array)
# т.к. в ряду кнопок, добавленных при помощи метода row, превышен лимит на их количество в ряду
# то метод insert добавит кнопку в новый ряд
url_kb.add(url_button1, url_button2).row(*buttons_array).insert(
    InlineKeyboardButton(text='Ссылка6', url='https://www.google.com'))


@dp.message_handler(commands='ссылки')
async def url_command(message: types.Message):
    await message.answer('Ссылочки', reply_markup=url_kb)


# при помощи callback_data боту передаются скрытые от пользователя данные боту, которые можно вытащить через специальный
# обработчик событий
inline_kb = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text='Нажми меня', callback_data='www'))\
    .add(InlineKeyboardButton(text='Like', callback_data='like_+1'),
         InlineKeyboardButton(text='Dislike', callback_data='like_-1'))


@dp.message_handler(commands='test')
async def test_command(message: types.Message):
    await message.answer('Инлайн кнопка', reply_markup=inline_kb)


# чтобы связать вызываемую функцию с инлайн кнопкой в text задается то, что было передано в параметре callback_data
# кнопки в результате выполнения функции Telegram ожидает ответа от бота (появляются часики в углу кнопки)
@dp.callback_query_handler(text='www')
async def www_call(callback_query: types.CallbackQuery):
    # можно, к примеру вызвать метод types.CallbackQuery.answer, чтобы в диалоге всплыла временная надпись
    # await callback_query.answer('Нажата инлайн кнопка')
    # или можно, к примеру вызвать метод types.CallbackQuery.message.answer, чтобы прислать ответное сообщение
    await callback_query.message.answer('Нажата инлайн кнопка')
    # но тогда необходимо вызвать types.CallbackQuery.answer с пустым аргументом
    # await callback_query.answer()
    # если указать аргумент, то будет отображена и всплывающая надпись
    await callback_query.answer('Текст появился и скрылся')
    # если добавить аргумент show_alert=True, то появится окно с сообщением, которое необходимо подтвердить,
    # нажав на OK
    await callback_query.answer('Текст появился и скрылся', show_alert=True)


# фильтрация событий нажатий кнопок по переданным из них данных
@dp.callback_query_handler(Text(startswith='like_'))
async def like_call(callback_query: types.CallbackQuery):
    # вытаскивание +1 или -1
    res = int(callback_query.data.split('_')[1])
    if f'{callback_query.from_user.id}' not in answers:
        answers[f'{callback_query.from_user.id}'] = res
        await callback_query.answer('Вы проголосовали')
    else:
        await callback_query.answer('Вы уже проголосовали', show_alert=True)


executor.start_polling(dp, skip_updates=True)
