from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# кнопки для клавиатуры, заменяющей обычную
# строки(команды) указанные при создании объектов кнопок будут отправлять при их нажатии
# и их нельзя подменить
b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Отправить где я', request_location=True)

# one_time_keyboard=True - входной параметр конструктора, после нажатия на одну из кнопок скроется клавиатура,
# но её можно восстановить нажав на кнопку с 4мя кружками в квадрате на клавиатуре(находится рядом с кнопкой
# прикрепления файлов и записи аудио-, видеосообщений
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# add добавляет ряд из одной кпонки, insert - в уже существующий ряд ещё кнопку
# kb_client.add(b1).add(b2).insert(b3)
# 3 кнопки в ряд
# kb_client.row(b1, b2, b3)
kb_client.add(b1).add(b2).add(b3)  # .row(b4, b5)
