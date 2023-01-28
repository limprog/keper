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
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from flask import Flask, render_template, session, request,  redirect, url_for, flash
import sqlite3
import os
from states import *
import requests
import asyncio



def get_db_connection():
    conn = sqlite3.connect(os.path.join('../database/database.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


app = Flask(__name__)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
states = States()
reg = {}


@app.route('/test', methods=['POST'])
def get_test():
    data = request.get_json()
    print(data)
    return ("ok")


@dp.message_handler(commands=['start'])
async def comand_start(message: types.Message):
    await message.answer(ANSWER_COM_START)


@dp.message_handler(commands=["help"])
async def comand_help(message: types.Message):
    await message.answer(ANSWER_COM_HELP)


@dp.message_handler(commands=["info"])
async def comand_info(message: types.Message):
    await message.answer(ANSWER_COM_INFO)


@dp.message_handler(commands=["insaider"])
async def comand_insaider(message: types.Message):
    await message.answer(ANSWER_COM_INSADER)


@dp.message_handler(commands=['reg'])
async def comand_reg(message: types.Message, state: FSMContext):
    if not reg:
        await message.answer("Для регестрации введдите свое имя")
        await states.fname.set()
    else:
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['fname']}")


@dp.message_handler(state=states.fname)
async def comand_reg_2(message: types.Message, state: FSMContext):
    await state.update_data(fname=message.text)
    await message.answer('Дальше введите никнейм')
    await states.sname.set()


@dp.message_handler(state=states.sname)
async def comand_reg_3(message: types.Message, state: FSMContext):
    await state.update_data(sname=message.text)
    await message.answer('Дальше введите email')
    await states.email.set()


@dp.message_handler(state=states.email)
async def comand_reg_4(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Дальше введите пароль')
    await states.cod.set()


@dp.message_handler(state=states.cod)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(cod=message.text)
    await message.answer('Потвердите пароль')
    await states.rcod.set()


@dp.message_handler(state=states.rcod)
async def comand_reg_6(message: types.Message, state: FSMContext):
    await state.update_data(rcod=message.text)
    data = await state.get_data()
    if data['cod'] == data['rcod']:
        await message.answer(f'Ваше имя {data["fname"]} \nВаш никнейм {data["sname"]} \nВаш email {data["email"]}' )
        global reg
        reg["fname"] = data["fname"]
        reg['sname'] = data['sname']
        reg['email'] = data['email']
        reg['tgid'] = message.from_user.id
        await message.answer("Все правельно?")
        await states.answer.set()
    else:
        await message.answer("Пароли не совпадают \nНачните сначала или повторите ввод проля\nнапешие пароль или повторить")
        await states.answer2.set()


@dp.message_handler(state=states.answer)
async def comand_reg_f(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    answer = data['answer'].strip().lower()
    if answer == "да":
        conn, cur = get_db_connection()
        tgid = message.from_user.id
        await message.answer("Регистрация окончина")
        conn.execute('INSERT INTO users (fname, sname, cod, email, tgid) VALUES (?, ?, ?, ?, ?)',
                     (data["fname"], data["sname"], data["cod"], data["email"], tgid,))
        conn.commit()
        conn.close()
        await state.finish()
    elif answer == "нет":
        await message.answer("Начните сначала")
        await message.answer("Для регестрации введдите свое имя")
        await states.fname.set()


@dp.message_handler(state=states.answer2)
async def comand_reg_r(message: types.Message, state: FSMContext):
    await state.update_data(answer2=message.text)

    data = await state.get_data()
    answer = data['answer2'].strip().lower()
    if sum([answer.find(i)!=-1 for i in ["повторить"]]):
        await message.answer("Начните сначала")
        await message.answer("Для регестрации введдите свое имя")
        await states.fname.set()
    elif sum([answer.find(i)!=-1 for i in ["пароль"]]):
        await message.answer("Начните c повтора пароля")
        await message.answer('Потвердите пароль')
        await states.rcod.set()


@dp.message_handler(commands=['auth'])
async def comand_auht_1(message: types.Message, state: FSMContext):
    if not reg:
        await message.answer("Для аунтофикации введдите свой email")
        await states.email_2.set()
    else:
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['fname']}")


@dp.message_handler(state=states.email_2)
async def comand_auht_2(message: types.Message, state: FSMContext):
    await state.update_data(email_2=message.text)
    await message.answer("Для аунтофикации введдите свой пароль")
    await states.cod_2.set()


@dp.message_handler(state=states.cod_2)
async def comand_auht_3(message: types.Message, state: FSMContext):
    await state.update_data(cod_2=message.text)
    data = await state.get_data()
    conn, cur = get_db_connection()
    # добавить проверку на существование
    cur.execute("SELECT * FROM users where email = (?)", (data['email_2'],))
    row = cur.fetchone()
    try:
        row['cod']
    except (TypeError):
        await message.answer("email не сушествует")
        await state.finish()
    print(row)
    print(row['cod'])
    tcod = row['cod']
    if tcod == data['cod_2']:
        global reg
        reg["fname"] = row["fname"]
        reg['sname'] = row['sname']
        reg['email'] = data['email_2']
        reg['tgid'] =  message.from_user.id
        await message.answer(f'Ваше имя {reg["fname"]} \nВаш никнейм {reg["sname"]} \nВаш email {reg["email"]}' )
        await message.answer("Все правельно?")
        await states.answer3.set()
    else:
        await message.answer("Пароли не савподают начнике с начала")
        await message.answer("Для аунтофикации введдите свой email")
        await states.email_2.set()


@dp.message_handler(state=states.answer3)
async def comand_auth_f(message: types.Message, state: FSMContext):
    await state.update_data(answer3=message.text)
    tgid = message.from_user.id
    data = await state.get_data()
    answer = data['answer3'].strip().lower()
    if sum([answer.find(i)!=-1 for i in ["да"]]):
        sql = f"UPDATE users SET tgid='{tgid}' WHERE email = '{data['email_2']}'"
        conn, cur = get_db_connection()
        cur.execute(sql)
        conn.commit()
        conn.close()
        await message.answer("Авторизация закончина")
    elif sum([answer.find(i)!=-1 for i in ["нет"]]):
        await message.answer("Начните c начала")
        await message.answer("Для аунтофикации введдите свой email")
        await states.email_2.set()


@dp.message_handler(commands=['akk'])
async def comand_akk(message: types.Message):
    await message.answer(f'Ваше имя {reg["fname"]} \nВаш никнейм {reg["sname"]} \nВаш email {reg["email"]}')


@dp.message_handler(commands=['rem'])
async def comand_akk(message: types.Message):
    await message.answer("Вы вышли из акаунта")
    global reg
    reg = {}



async def on_startup(x):
    asyncio.create_task(asyncio.to_thread(app.run))

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)