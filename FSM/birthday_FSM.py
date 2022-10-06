from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMInputDate(StatesGroup):
    date = State()
    name = State()
    change_date = State()
    ticket_state = State()