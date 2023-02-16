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
button_h1 = KeyboardButton("mon")
button_h2 = KeyboardButton("tue")
button_h3 = KeyboardButton("wed")
button_h4 = KeyboardButton("thu")
button_h5 = KeyboardButton("fri")
button_h6 = KeyboardButton("sat")
button_h7 = KeyboardButton("sun")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button_h1,button_h2, button_h3, button_h4,button_h5, button_h6,button_h7)

#await bot.send_message(message.from_user.id, "test message")
model = torch.load(os.path.join('../net/best_scr_v3_shufflenet_v2.pth'), map_location={'cuda:0': 'cpu'})

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
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['nickname']}")


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
    reg1 = {}
    answer = data['answer'].strip().lower()
    if answer == "да":
        tgid = message.from_user.id
        reg1['name'] = data['name']
        reg1['nickname'] = data['nickname']
        reg1['position'] = data['position']
        reg1['timetable'] = data['timetable1'] + " " + data['timetable2']
        reg1['cod'] = data["cod"]
        reg1["tgid"] = tgid
        r = requests.post(url +"/reg", data=reg1)
        global reg
        reg = reg1
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
        await states.name.set()
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
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['nickname']}")


@dp.message_handler(state=states.nickname2)
async def comand_auht_2(message: types.Message, state: FSMContext):
    await state.update_data(nickname2=message.text)
    await message.answer("Для аунтофикации введдите свой пароль")
    await states.cod_2.set()


@dp.message_handler(state=states.cod_2)
async def comand_auht_3(message: types.Message, state: FSMContext,):
    await state.update_data(cod=message.text)
    tgid = message.from_user.id
    data = await state.get_data()
    reg1 = {}
    reg1['nickname'] = data['nickname2']
    reg1['cod'] = data['cod']
    reg1['tgid'] = tgid
    r = requests.post(url +"/auth", data=reg1)
    if r.status_code == 418:
        await message.answer("Такого никнейма нет")
        await state.finish()
    elif r.status_code == 201:
        await message.answer(f"все хорошо вы авторизовоны под никнейм {reg1['nickname']}")
        reg1['name'] = r.text
        global reg
        reg = reg1
        await state.finish()
        print(await state.get_data())

    elif r.status_code == 401:
        await message.answer("Неправельный пароль \n")
        await state.finish()


@dp.message_handler(commands=['akk'])
async def comand_akk(message: types.Message, state: FSMContext):
    if reg:
        data = await state.get_data()
        print(data)
        if not reg:
            await message.answer(f'Ваше имя {reg["name"]} \nВаш никнейм {reg["nickname"]} ')
        else:
            await message.answer(f'Ваше имя {reg["name"]} \nВаш никнейм {reg["nickname"]} ')


@dp.message_handler(commands=['rem'])
async def comand_akk(message: types.Message, state: FSMContext):
    await message.answer("Вы вышли из акаунта")
    global reg
    reg= {}
    await state.reset()


@dp.message_handler(commands=['del'])
async def com_del(message: types.Message, state: FSMContext):
    if reg:
        data = await state.get_data()
        await message.answer("вы уверенны что хотите удалить аккаунт")
        await states.del1.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")

@dp.message_handler(state=states.del1)
async def del_1(message: types.Message, state: FSMContext):
    await state.update_data(del1=message.text)
    data = await state.get_data()
    answer = data['del1'].strip().lower()
    if answer == "да":
        global reg
        r = requests.post(url +'/del', data=reg)
        await message.answer("аккаунт удалён")
        reg = {}
        await state.finish()
    else:
        await state.finish()


@dp.message_handler(commands=['c_name'])
async def comand_chan_name(message: types.Message, state: FSMContext):
    if reg:
        await message.answer("вы уверенны что хотите изменить аккаунт")
        await states.chan_name.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")



@dp.message_handler(state=states.chan_name)
async def chan_name(message: types.Message, state: FSMContext):
    await state.update_data(chan_name=message.text)
    data = await state.get_data()
    answer = data['chan_name'].strip().lower()
    if answer == 'да':
        await message.answer("Напишите новое имя")
        await states.chan_name2.set()
    else:
        await message.answer("Все хорошо")
        await state.finish()


@dp.message_handler(state=states.chan_name2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_name2=message.text)
    data = await state.get_data()
    reg1 = {}
    global reg
    reg1["nickname"] = reg['nickname']
    reg1['newname'] = data['chan_name2']
    r = requests.post(url+"/chan/name", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        reg["name"] = data['chan_name2']
        await state.finish()


@dp.message_handler(commands=['c_nickname'])
async def comand_chan_name(message: types.Message, state: FSMContext):
    if reg:
        await message.answer("вы уверенны что хотите изменить аккаунт")
        await states.chan_nickname.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")


@dp.message_handler(state=states.chan_nickname)
async def chan_name(message: types.Message, state: FSMContext):
    await state.update_data(chan_nickname=message.text)
    data = await state.get_data()
    answer = data['chan_nickname'].strip().lower()
    if answer == 'да':
        await message.answer("Напишите новый никнем")
        await states.chan_nickname2.set()
    else:
        await message.answer("Все хорошо")
        await state.finish()


@dp.message_handler(state=states.chan_nickname2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_nickname2=message.text)
    data = await state.get_data()
    reg1 = {}
    global reg
    reg1["nickname"] = reg['nickname']
    reg1['newnickname'] = data['chan_nickname2']
    r = requests.post(url+"/chan/nickname", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        reg["name"] = data['chan_nicknamе2']
        await state.finish()


@dp.message_handler(commands=['c_cod'])
async def comand_chan_name(message: types.Message, state: FSMContext):
    if reg:
        await message.answer("вы уверенны что хотите изменить аккаунт")
        await states.chan_cod.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")



@dp.message_handler(state=states.chan_cod)
async def chan_name(message: types.Message, state: FSMContext):
    await state.update_data(chan_cod=message.text)
    data = await state.get_data()
    answer = data['chan_cod'].strip().lower()
    if answer == 'да':
        await message.answer("Напишите новый пароль")
        await states.chan_cod2.set()
    else:
        await message.answer("Все хорошо")
        await state.finish()


@dp.message_handler(state=states.chan_cod2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_cod2=message.text)
    data = await state.get_data()
    reg1 = {}
    global reg
    reg1["nickname"] = reg['nickname']
    reg1['newcod'] = data['chan_cod2']
    r = requests.post(url+"/chan/cod", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        reg["name"] = data['chan_cod2']
        await state.finish()


@dp.message_handler(commands=['c_time'])
async def comand_chan_name(message: types.Message, state: FSMContext):
    if reg:
        await message.answer("вы уверенны что хотите изменить аккаунт")
        await states.chan_time.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")



@dp.message_handler(state=states.chan_time)
async def chan_name(message: types.Message, state: FSMContext):
    await state.update_data(chan_time=message.text)
    data = await state.get_data()
    answer = data['chan_time'].strip().lower()
    if answer == 'да':
        await message.answer('Дальше введите рабочий день недели', reply_markup=greet_kb)
        await states.chan_time2.set()
    else:
        await message.answer("Все хорошо")
        await state.finish()


@dp.message_handler(state=states.chan_time2)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(chan_time2=message.text)
    await message.answer('Дальше введите час начара работы в формате 13:23', reply_markup=ReplyKeyboardRemove())
    await states.chan_time3.set()


@dp.message_handler(state=states.chan_time3)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_cod3=message.text)
    data = await state.get_data()
    reg1 = {}
    global reg
    reg1["nickname"] = reg['nickname']
    reg1['newtime'] = data['chan_time2']+ " " +data['chan_cod3']
    r = requests.post(url + "/chan/time", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        reg["name"] = data['chan_time3']
        await state.finish()


@dp.message_handler(commands=['room_reg'])
async def room_reg(message: types.Message, state: FSMContext):
    if reg:
        await message.answer('для регистации наберите номер кабинета')
        await states.room_name.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")


@dp.message_handler(state=states.room_name)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(room_name=message.text)
    data = await state.get_data()
    room = {}
    room['op_name'] = reg['op_name']
    room['nickname'] = reg['nickname']
    room['name'] = data['room_name']
    r = requests.post(url+"/room/reg", data=room)
    if r.status_code == 201:
        await message.answer('все хорошо')
        await state.finish()
    else:
        await message.answer('все полохо')
        await state.finish()


@dp.message_handler(commands=['reg_op'])
async def reg_op(message: types.Message, state: FSMContext):
    if reg:
        await message.answer('для регистации наберите название организации')
        await states.op_name.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")

@dp.message_handler(state=states.op_name)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(op_name=message.text)
    await message.answer('для регистации наберите город нахождения организации')
    await states.op_city.set()


@dp.message_handler(state=states.op_city)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(op_city=message.text)
    await message.answer('Придумайте пароль')
    await states.op_cod.set()


@dp.message_handler(state=states.op_cod)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(op_cod=message.text)
    await message.answer('Повторите пароль')
    await states.op_rcod.set()


@dp.message_handler(state=states.op_rcod)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(op_rcod=message.text)
    data = await state.get_data()
    if data['op_cod'] == data['op_rcod']:
        global reg
        reg["op_city"] = data['op_city']
        reg['op_name'] = data['op_name']
        reg['op_cod'] = data['op_cod']
        r = requests.post(url+"/op/reg", data=reg)
        if r.status_code == 201:
            await message.answer('все хорошо')
            await state.finish()
        else:
            await message.answer('все полохо')
            await state.finish()
    else:
        await message.answer("Пароли не совпадают \nНачните сначала или повторите ввод проля\nнапешие пароль или повторить")
        await states.answer4.set()

@dp.message_handler(state=states.answer4)
async def comand_reg_r(message: types.Message, state: FSMContext):
    await state.update_data(answer4=message.text)
    data = await state.get_data()
    answer = data['answer4'].strip().lower()
    if sum([answer.find(i)!=-1 for i in ["повторить"]]):
        await message.answer("Начните сначала")
        await message.answer('для регистации наберите город нахождения организации')
        await states.op_name.set()
    elif sum([answer.find(i)!=-1 for i in ["пароль"]]):
        await message.answer("Начните c повтора пароля")
        await message.answer('Потвердите пароль')
        await states.op_rcod.set()

@dp.message_handler(commands=['auth_op'])
async def comand_auht_op(message: types.Message, state: FSMContext):
    if reg:
        await message.answer('напешите имя организации')
        await states.op_name2.set()


@dp.message_handler(state=states.op_name2)
async def comand_auht_op(message: types.Message, state: FSMContext):
    await state.update_data(op_name2=message.text)
    await message.answer('Введите пароль')
    await states.op_cod2.set()


@dp.message_handler(state=states.op_cod2)
async def comand_auht_op(message: types.Message, state: FSMContext):
    await state.update_data(op_cod2=message.text)
    data = await state.get_data()
    reg['op_name'] = data['op_name2']
    reg['op_cod'] = data['op_cod2']
    r = requests.post(url+'/op/auth', data=reg)
    if r.status_code == 201:
        await message.answer('Все хорошо')
        print(reg['op_name'])
        await state.finish()
    elif r.status_code == 418:
        await message.answer('Все неправельный пароль')
        await state.finish()


@dp.message_handler(commands=['stat'])
async def commad_stat(message: types.Message, state: FSMContext):
    await message.answer("Введите id компа, с которого были сделаны сегодня скриншоты")
    await states.stat_id.set()


@dp.message_handler(state=states.stat_id)
async def commad_stat(message: types.Message, state: FSMContext):
    await state.update_data(stat_id=message.text)
    data = await state.get_data()
    stat = {}
    print(data["stat_id"])
    stat["stat_id"] = data["stat_id"]
    r = requests.post(url+"/stat/today", data=stat)
    if r.status_code == 202:
        photo = InputFile(os.path.join("../server/loogs/2023-02-09", data["stat_id"]+'.png'))
        await bot.send_photo(message.from_user.id, photo=photo)
        await state.finish()

    else:
        await message.answer("404")


async def scrin(file, tgid, id,result):
    photo = InputFile(os.path.join("../server/img", file))
    if result['pred_class'] != "Game":
        await bot.send_photo(tgid, photo=photo)
        await bot.send_message(tgid, f"Компьютер с id {id} занимается работой в {result['pred_class']}")
        await bot.send_message(tgid, text="😻")
    else:
        await bot.send_photo(tgid, photo=photo)
        await bot.send_message(tgid, f"Компьютер с id {id}: обнаружена подозрительная активность класса {result['pred_class']}")
        await bot.send_message(tgid, text="😭")


if __name__ == '__main__':
    executor.start_polling(dp,  skip_updates=True)