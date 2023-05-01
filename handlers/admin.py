from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bot
from keyboards import admin_kb
from database import sqlite_bd

ID = None


# класс машины состояния
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
# чтобы сработала регистрация админки необходимо в группе с ботои
# прописать команду /moderator (в ответ на неё прийдёт личное сообщение от бота) а потом в личных сообщениях с ботом
# ввести команду /Загрузить
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    print(f'ID is {ID}')
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.kb_admin)
    await message.delete()


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    # установка машины состояния в состояние загрузки фото
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# сработает при любом состоянии машины состояния по команде отмена
# @dp.message_handler(state="*", commands='отмена')
# фильтр по слову тоже в любом состоянии машины состояний
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state=FSMContext):
    # сохранение в контекст информацию о загруженном фото
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь введи название')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state=FSMContext):
    # сохранение в контекст информацию о названии пиццы
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи описание')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state=FSMContext):
    # сохранение в контекст информацию о названии пиццы
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь укажи цену')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state=FSMContext):
    # сохранение в контекст информацию о названии пиццы
    async with state.proxy() as data:
        data['price'] = float(message.text)
    async with state.proxy() as data:
        await message.reply(str(data))
    # после этой команды сбрасывается состояние у машины состояния
    # поэтому все манипуляции с данными необходимо выполнить до этой команды
    await sqlite_bd.sql_add_command(state)
    await state.finish()


# для примера хэндлера с фильтром
async def test_filter(message: types.Message):
    await message.reply('passed message by filter')


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_bd.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


# @dp.message_handler(commands='Удалить', state=None)
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_bd.sql_only_read_all()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(
                message.from_user.id,
                text='^^^',
                reply_markup=InlineKeyboardMarkup()
                .add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    # добавление хэндлера с фильтром сообщений начинающихся с hello
    dp.register_message_handler(test_filter, lambda message: message.text.startswith('hello'))
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
