import logging
import sqlite3
import os
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
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
greet_kb.add(button_h1, button_h2, button_h3, button_h4, button_h5, button_h6, button_h7)
# Основные команды для аккаунта
akk_btn = InlineKeyboardButton('Информация об аккаунте', callback_data='akk')
rem_btn = InlineKeyboardButton('Выход из аккаунта', callback_data='rem')
del_btn = InlineKeyboardButton("Удаление аккаунта", callback_data='del')
osn_com_to_c_bnt = InlineKeyboardButton("Изменение аккаунта >>", callback_data='osn_com_to_c')
osn_com_to_stat_bnt = InlineKeyboardButton("<< Статистика", callback_data='osn_com_to_stat')
osn_com_kb = InlineKeyboardMarkup()
osn_com_kb.row(rem_btn, del_btn)
osn_com_kb.row(akk_btn)
osn_com_kb.row(osn_com_to_stat_bnt,osn_com_to_c_bnt)
# Изменение аккаунта
с_name_btn = InlineKeyboardButton("Изменение имени", callback_data='с_name')
с_nickname_btn = InlineKeyboardButton("Изменение никнейма", callback_data='с_nickname')
c_cod_btn = InlineKeyboardButton("Изменение пороля", callback_data='с_cod')
c_time_btn = InlineKeyboardButton("Изменение расписания", callback_data='с_time')
c_to_osn_com = InlineKeyboardButton("<< Основные команды", callback_data='с_to_osn_com')
c_to_org_com = InlineKeyboardButton("Организационные команды >>", callback_data='с_to_org_com')
change_kb = InlineKeyboardMarkup().add(с_name_btn, с_nickname_btn)
change_kb.add(c_cod_btn, c_time_btn)
change_kb.add(c_to_osn_com, c_to_org_com)
# Организациооные команды
reg_op_btn = InlineKeyboardButton("Регистрация организации", callback_data='reg_op')
auth_op_btn = InlineKeyboardButton("Авторизация в организацию", callback_data='auth_op')
room_reg_btn = InlineKeyboardButton("Регистрация комнаты", callback_data='reg_room')
org_com_to_c_bth = InlineKeyboardButton("<< Изменение аккаунта", callback_data='org_com_to_c')
org_com_to_stat_bth = InlineKeyboardButton("Статистика >>", callback_data="org_com_to_stat")
org_com_kb = InlineKeyboardMarkup()
org_com_kb.add(reg_op_btn, auth_op_btn)
org_com_kb.add(room_reg_btn)
org_com_kb.add(org_com_to_c_bth, org_com_to_stat_bth)
# Статистика
stat_today_btn = InlineKeyboardButton("Статистика по компютеру", callback_data="stat_today")
stat_class_btn = InlineKeyboardButton("Статистика по классам", callback_data="stat_class" )
stat_to_org_com_btn = InlineKeyboardButton("<< Организационные команды", callback_data="stat_to_org_com")
stat_to_osn_com_btn = InlineKeyboardButton("Основные команды >>", callback_data="stat_to_osn_com")
stat_kb = InlineKeyboardMarkup().add(stat_today_btn)
stat_kb.add(stat_class_btn)
stat_kb.add(stat_to_org_com_btn,stat_to_osn_com_btn )
# await bot.send_message(message.from_user.id, "test message")
model = torch.load(os.path.join('../net/best_scr_v3_shufflenet_v2.pth'), map_location={'cuda:0': 'cpu'})





@dp.message_handler(commands=['start'], state='*')
async def comand_start(message: types.Message, state: FSMContext):
    reg = await state.get_data()
    if not reg:
        await message.answer(ANSWER_COM_START)
    else:
        await message.answer("Основные команды для аккаунта", reply_markup=osn_com_kb)

@dp.message_handler(commands=["help"], state='*')
async def comand_help(message: types.Message):
    if not reg:
        await message.answer(ANSWER_COM_HELP)



@dp.message_handler(commands=["info"], state='*')
async def comand_info(message: types.Message):
    await message.answer(ANSWER_COM_INFO)


@dp.message_handler(commands=["insaider"], state='*')
async def comand_insaider(message: types.Message):
    await message.answer(ANSWER_COM_INSADER)


@dp.message_handler(commands=['akk'], state='*')
async def comand_akk(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'Ваше имя {data["name"]} \nВаш никнейм {data["nickname"]} ')


@dp.message_handler(commands=['rem'], state='*')
async def comand_akk(message: types.Message, state: FSMContext):
    await message.answer("Вы вышли из акаунта")
    await state.finish()


@dp.message_handler(commands=['del'], state='*')
async def com_del(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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
        r = requests.post(url + '/del', data=data)
        await message.answer("аккаунт удалён")
        await state.finish()
    else:
        pass


@dp.message_handler(commands=['c_name'], state='*')
async def comand_chan_name(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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



@dp.message_handler(state=states.chan_name2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_name2=message.text)
    data = await state.get_data()
    reg1 = {}

    reg1["nickname"] = data['nickname']
    reg1['newname'] = data['chan_name2']
    r = requests.post(url + "/chan/name", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        await state.update_data(name=data['chan_name2'])




@dp.message_handler(commands=['c_nickname'], state='*')
async def comand_chan_name(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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


@dp.message_handler(state=states.chan_nickname2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_nickname2=message.text)
    data = await state.get_data()
    reg1 = {}
    reg1["nickname"] = data['nickname']
    reg1['newnickname'] = data['chan_nickname2']
    r = requests.post(url + "/chan/nickname", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")
        await state.update_data(nickname=data['chan_nickname2'])



@dp.message_handler(commands=['c_cod'], state='*')
async def comand_chan_name(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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



@dp.message_handler(state=states.chan_cod2)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(chan_cod2=message.text)
    data = await state.get_data()
    reg1 = {}
    reg1["nickname"] = data['nickname']
    reg1['newcod'] = data['chan_cod2']
    r = requests.post(url + "/chan/cod", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")



@dp.message_handler(commands=['c_time'], state='*')
async def comand_chan_name(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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
    reg1["nickname"] = data['nickname']
    reg1['newtime'] = data['chan_time2'] + " " + data['chan_cod3']
    r = requests.post(url + "/chan/time", data=reg1)
    if r.status_code == 201:
        await message.answer("Все хорошо")


@dp.message_handler(commands=['room_reg'], state='*')
async def room_reg(message: types.Message, state: FSMContext):
    reg = await state.get_data()
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
    room['op_name'] = data['op_name']
    room['nickname'] = data['nickname']
    room['name'] = data['room_name']
    r = requests.post(url + "/room/reg", data=room)
    if r.status_code == 201:
        await message.answer('все хорошо')

    else:
        await message.answer('все полохо')



@dp.message_handler(commands=['reg_op'],  state='*')
async def reg_op(message: types.Message, state: FSMContext):
    reg = await state.get_data()
    if reg:
        await message.answer('Для регистрации наберите название организации')
        await states.op_name.set()
    else:
        await message.answer("Зарегестрируйтесь или войдите")


@dp.message_handler(state=states.op_name)
async def chan_name2(message: types.Message, state: FSMContext):
    await state.update_data(op_name=message.text)
    await message.answer('Для регистрации наберите город нахождения организации')
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
        reg = {}
        reg["op_city"] = data['op_city']
        reg['op_name'] = data['op_name']
        reg['op_cod'] = data['op_cod']
        r = requests.post(url + "/op/reg", data=reg)
        if r.status_code == 201:
            await message.answer('все хорошо')

        else:
            await message.answer('все полохо')

    else:
        await message.answer("Пароли не совпадают \nНачните сначала или повторите ввод проля\nнапешие пароль или повторить")
        await states.answer4.set()


@dp.message_handler(state=states.answer4)
async def comand_reg_r(message: types.Message, state: FSMContext):
    await state.update_data(answer4=message.text)
    data = await state.get_data()
    answer = data['answer4'].strip().lower()
    if sum([answer.find(i) != -1 for i in ["повторить"]]):
        await message.answer("Начните сначала")
        await message.answer('Для регистрации наберите город нахождения организации')
        await states.op_name.set()
    elif sum([answer.find(i) != -1 for i in ["пароль"]]):
        await message.answer("Начните c повтора пароля")
        await message.answer('Подтвердите пароль')
        await states.op_rcod.set()


@dp.message_handler(commands=['auth_op'], state='*')
async def comand_auht_op(message: types.Message, state: FSMContext):
    reg = await state.get_data()
    if reg:
        await message.answer('Напишите название организации')
        await states.op_name2.set()
    else:
        print("error")


@dp.message_handler(state=states.op_name2)
async def comand_auht_op(message: types.Message, state: FSMContext):
    await state.update_data(op_name=message.text)
    await message.answer('Введите пароль')
    await states.op_cod2.set()


@dp.message_handler(state=states.op_cod2)
async def comand_auht_op(message: types.Message, state: FSMContext):
    await state.update_data(op_cod=message.text)
    data = await state.get_data()
    reg['op_name'] = data['op_name']
    reg['op_cod'] = data['op_cod']
    r = requests.post(url + '/op/auth', data=reg)
    if r.status_code == 201:
        await message.answer('Все хорошо')
    elif r.status_code == 418:
        await message.answer('Неправильный пароль')


@dp.message_handler(commands=['stat'], state='*')
async def commad_stat(message: types.Message, state: FSMContext):
    await message.answer("Введите id компа, с которого были сделаны сегодня скриншоты")
    await states.stat_id.set()


@dp.message_handler(state=states.stat_id)
async def commad_stat(message: types.Message, state: FSMContext):
    await state.update_data(stat_id=message.text)
    data = await state.get_data()
    stat = {}
    stat["stat_id"] = data["stat_id"]
    r = requests.post(url + "/stat/today", data=stat)
    if r.status_code == 202:
        photo = InputFile(os.path.join("../server/loogs/2023-02-09", data["stat_id"] + '.png'))
        await bot.send_photo(message.from_user.id, photo=photo)
    else:
        await message.answer("404")


@dp.message_handler(commands=['stat_room'], state='*')
async def commad_stat_room(message: types.Message, state: FSMContext):
    await message.answer("Введите номер комнаты")
    await states.room_nb.set()


@dp.message_handler(state='room_nb')
async def commad_stat_room_1(message: types.Message, state: FSMContext):
    await state.update_data(room_nb=message.text)
    data = await state.get_data()
    room = {}
    room['nickname'] = data['nickname']
    room['room_nb'] = data['room_nb']
    r = requests.post(url+"/stat/class", data=room)
    if r.status_code == 201:
        await message.answer("ТиПо СтАтА")

@dp.message_handler(commands=['reg'], state='*')
async def comand_reg(message: types.Message, state: FSMContext):
    reg = await state.get_data()
    if not reg:
        await message.answer("Для регистрации введите свое имя")
        await states.name.set()
    else:
        await message.answer(f"В аккаунт выполнен вход.\nВаш никнейм: {reg['nickname']}")


@dp.message_handler(state=states.name)
async def comand_reg_2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Дальше введите никнейм')
    await states.nickname.set()


@dp.message_handler(state=states.nickname)
async def comand_reg_3(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer('Дальше введите свою должность')
    await states.position.set()


@dp.message_handler(state=states.position)
async def comand_reg_4(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer('Дальше введите рабочий день недели', reply_markup=greet_kb)
    await states.timetable1.set()


@dp.message_handler(state=states.timetable1)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(timetable1=message.text)
    await message.answer('Дальше введите час начала работы в формате 13:23', reply_markup=ReplyKeyboardRemove())
    await states.timetable2.set()


@dp.message_handler(state=states.timetable2)
async def comand_reg_5(message: types.Message, state: FSMContext):
    await state.update_data(timetable2=message.text)
    await message.answer('Дальше введите пароль')
    await states.cod.set()


@dp.message_handler(state=states.cod)
async def comand_reg_6(message: types.Message, state: FSMContext):
    await state.update_data(cod=message.text)
    await message.answer('Подтвердите пароль')
    await states.rcod.set()


@dp.message_handler(state=states.rcod)
async def comand_reg_7(message: types.Message, state: FSMContext):
    await state.update_data(rcod=message.text)
    data = await state.get_data()
    if data['cod'] == data['rcod']:
        await message.answer(
            f'Ваше имя {data["name"]} \nВаш никнейм {data["nickname"]} \nВаше место работы{data["position"]}, \nДни работы {data["timetable1"]}, \nВремя начала {data["timetable2"]}')
        await message.answer("Все правильно?")
        await states.answer.set()
    else:
        await message.answer(
            "Пароли не совпадают \nНачните сначала или повторите ввод проля\nнапешие пароль или повторить")
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
        r = requests.post(url + "/reg", data=reg1)
        if r.status_code == 204:
            await message.answer("все хорошо")
            print(await state.get_data())

    elif answer == "нет":
        await message.answer("Начните сначала.")
        await message.answer("Для регистрации введите свое имя.")
        await states.fname.set()


@dp.message_handler(state=states.answer2)
async def comand_reg_r(message: types.Message, state: FSMContext):
    await state.update_data(answer2=message.text)

    data = await state.get_data()
    answer = data['answer2'].strip().lower()
    if sum([answer.find(i) != -1 for i in ["повторить"]]):
        await message.answer("Начните сначала")
        await message.answer("Для регистрации введите свое имя")
        await states.name.set()
    elif sum([answer.find(i) != -1 for i in ["пароль"]]):
        await message.answer("Начните c повтора пароля")
        await message.answer('Потвердите пароль')
        await states.rcod.set()


@dp.message_handler(commands=['auth'], state='*')
async def comand_auht_1(message: types.Message, state: FSMContext):
    if not reg:
        await message.answer("Для аунтофикации введдите свой никнейм")
        await states.nickname2.set()
    else:
        await message.answer(f"В аккаунт выполнин вход\nВаш никнейм: {reg['nickname']}")


@dp.message_handler(state=states.nickname2)
async def comand_auht_2(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Для аунтентофикации введите свой пароль")
    await states.cod_2.set()


@dp.message_handler(state=states.cod_2)
async def comand_auht_3(message: types.Message, state: FSMContext, ):
    await state.update_data(cod=message.text)
    tgid = message.from_user.id
    data = await state.get_data()
    reg1 = {}
    reg1['nickname'] = data['nickname']
    reg1['cod'] = data['cod']
    reg1['tgid'] = tgid
    r = requests.post(url + "/auth", data=reg1)
    if r.status_code == 418:
        await message.answer("Такого никнейма нет")
    elif r.status_code == 201:
        await message.answer(f"все хорошо вы авторизовоны под никнейм {reg1['nickname']}")
        data = r.json()
        await state.update_data(name=data["name"])


    elif r.status_code == 401:
        await message.answer("Неправельный пароль \n")


@dp.callback_query_handler(lambda c: c.data == 'akk')
async def change(message: types.Message, callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


async def scrin(file, tgid, id, result):
    photo = InputFile(os.path.join("../server/img", file))
    if result['pred_class'] != "Game":
        await bot.send_photo(tgid, photo=photo)
        await bot.send_message(tgid, f"Компьютер с id {id} занимается работой в {result['pred_class']}")
        await bot.send_message(tgid, text="😻")
    else:
        await bot.send_photo(tgid, photo=photo)
        await bot.send_message(tgid,
                               f"Компьютер с id {id}: обнаружена подозрительная активность класса {result['pred_class']}")
        await bot.send_message(tgid, text="😭")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
