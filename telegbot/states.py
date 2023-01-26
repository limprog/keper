from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    reg = State()
    fname = State()
    sname = State()
    email = State()
    cod = State()
    rcod = State()
    answer = State()
    answer2 = State()
    loh = State()
    email_2 = State()
    cod_2 = State()
    loh_2 = State()
    answer3 = State()