from aiogram.dispatcher.filters.state import StatesGroup, State


class Replenish(StatesGroup):
    set_amount_state = State()
