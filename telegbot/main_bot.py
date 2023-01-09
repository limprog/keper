'''
Этот фаил для того что-бы бот мог работать
'''

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hide_link
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from constants import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def comand_start(message: types.Message):
    await message.answer(ANSWER_COM_START)


@dp.message_handler(content_types=['new_chat_member'])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("start_prog", "Запустить програму"),
        types.BotCommand("insaider", "Инфа о новйх обнавлениях"),
        types.BotCommand("info", ""),
    ])



if __name__ == '__main__':
    executor.start_polling(dp)