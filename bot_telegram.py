# утилита для запуска работы бота
from aiogram.utils import executor
from create_bot import dp
from database import sqlite_bd


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_bd.sql_start()


from handlers import client, other, admin

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

# должен быть последним, т.к. реагирует на все команды/сообщения
other.register_handlers_other(dp)

# существует 2 режима работы бота:
# LongPolling - программа с ботом сама опрашивает сервер Telegram об имеющихся событиях
# на которые может реагировать бот. Основной минус - если сеть отвалится то программа вылетает
# и надо перезапускать
# WebHook - должен быть создан сервер на который будут приходить запросы от сервера Telegram
# в соответствии с соответствующим API
# skip_updates - параметр для игнорирования запросов поступивших боту, когда он был офлайн
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
