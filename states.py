from aiogram.fsm.state import State, StatesGroup


class BookingForm(StatesGroup):
    name = State()
    phone = State()