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
    del1 = State()
    chan_name = State()
    chan_name2= State()
    chan_nickname = State()
    chan_nickname2 = State()
    chan_cod = State()
    chan_cod2 = State()
    chan_time = State()
    chan_time2 = State()
    chan_time3 = State()
    room_name = State()
    op_name = State()
    op_city = State()
    op_cod = State()
    op_rcod = State()
    op_name2 = State()
    op_cod2 = State()
    answer4 = State()
    stat_id = State()
    id = State()
    roon_rb = State()
    decod = State()
    debug = State()