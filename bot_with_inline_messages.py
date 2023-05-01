import hashlib
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from aiogram.utils import executor

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


# улавливает события-обращения к боту пои помощи inline-сообщений
# перед тем как начать работать с этой функциональностью надо при помощи BotFather
# включить inline-режим /setinline  для нужного бота
@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = 'https://ru.wikipedia.org/wiki/' + text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [InlineQueryResultArticle(
        id=result_id,
        title='Статья Wikipedia:',
        url=link,
        input_message_content=InputTextMessageContent(
            message_text=link
        )
    )]
    await query.answer(articles, cache_time=1, is_personal=True)


executor.start_polling(dp, skip_updates=True)
