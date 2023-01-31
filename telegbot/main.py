import logging
import sqlite3
import os
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

import torch
import torchvision
import torchvision.transforms as transforms
from mmcls.apis import inference_model, init_model, show_result_pyplot

from telegbot.constants import *
from telegbot.states import *

url = 'http://127.0.0.1:5000'


loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
states = States()
reg = {}
button_h1 = KeyboardButton("Mon")
button_h2 = KeyboardButton("Tue")
button_h3 = KeyboardButton("Wed")
button_h4 = KeyboardButton("Thu")
button_h5 = KeyboardButton("Fri")
button_h6 = KeyboardButton("Sat")
button_h7 = KeyboardButton("Sun")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button_h1,button_h2, button_h3, button_h4,button_h5, button_h6,button_h7)

#await bot.send_message(message.from_user.id, "test message")


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
        await states.name.set()
    else:
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм:")


@dp.message_handler(state=states.name)
async def comand_reg_2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Дальше введите никнейм')
    await states.nickname.set()


@dp.message_handler(state=states.nickname)
async def comand_reg_3(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer('Дальше введите совю должность')
    await states.position.set()


@dp.message_handler(state=states.position)
async def comand_reg_4(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer('Дальше введите рабочий день недели', reply_markup=greet_kb)
    await states.timetable1.set()


@dp.message_handler(state=states.timetable1)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(timetable1=message.text)
    await message.answer('Дальше введите час начара работы в формате 13:23', reply_markup=ReplyKeyboardRemove())
    await states.timetable2.set()


@dp.message_handler(state=states.timetable2)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(timetable2=message.text)
    await message.answer('Дальше введите пароль')
    await states.cod.set()


@dp.message_handler(state=states.cod)
async def comand_reg_6(message: types.Message, state: FSMContext):
    await state.update_data(cod=message.text)
    await message.answer('Потвердите пароль')
    await states.rcod.set()


@dp.message_handler(state=states.rcod)
async def comand_reg_7(message: types.Message, state: FSMContext):
    await state.update_data(rcod=message.text)
    data = await state.get_data()
    if data['cod'] == data['rcod']:
        await message.answer(f'Ваше имя {data["name"]} \nВаш никнейм {data["nickname"]} \nВаше место работы{data["position"]}, \nДни работы {data["timetable1"]}, \nВремя начала {data["timetable2"]}' )
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
        tgid = message.from_user.id
        reg['name'] = data['name']
        reg['nickname'] = data['nickname']
        reg['position'] = data['position']
        reg['timetable'] = data['timetable1']+" "+data['timetable2']
        reg['cod'] = data["cod"]
        reg["tgid"] = tgid
        r = requests.post(url+"/reg", data=reg)
        await message.answer("Начните сначала")
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
        await message.answer("Для аунтофикации введдите свой никнейм")
        await states.nickname2.set()
    else:
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['fname']}")


@dp.message_handler(state=states.nickname2)
async def comand_auht_2(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Для аунтофикации введдите свой пароль")
    await states.cod_2.set()


@dp.message_handler(state=states.cod_2)
async def comand_auht_3(message: types.Message, state: FSMContext):
    await state.update_data(cod_2=message.text)
    data = await state.get_data()




@dp.message_handler(state=states.answer3)
async def comand_auth_f(message: types.Message, state: FSMContext):
    await state.update_data(answer3=message.text)
    tgid = message.from_user.id
    data = await state.get_data()
    answer = data['answer3'].strip().lower()
    if sum([answer.find(i)!=-1 for i in ["да"]]):
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

async def scrin(file, tgid):
    photo = InputFile(os.path.join("../server", file))
    model = torch.load(os.path.join('../net/best_scr_v3_shufflenet_v2.pth'), map_location={'cuda:0': 'cpu'})
    result = inference_model(model, os.path.join("../server", file))
    await bot.send_photo(tgid, photo=photo)
    await bot.send_message(tgid, result['pred_class'])

if __name__ == '__main__':
    executor.start_polling(dp,  skip_updates=True)