from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from create_bot import bot


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
    await bot.send_message(message.from_user.id, 'Что хозяин надо???')
    await message.delete()


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    print(f'message.from_user.id is {message.from_user.id}')
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
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
