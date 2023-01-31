from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    reg = State()
    name = State()
    nickname = State()
    position = State()
    timetable1 = State()
    timetable2 = State()
    cod = State()
    rcod = State()
    answer = State()
    answer2 = State()
    loh = State()
    nickname2 = State()
    cod_2 = State()
    loh_2 = State()
    answer3 = State()