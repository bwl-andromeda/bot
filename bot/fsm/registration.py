from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    fio = State()
    phone = State()
