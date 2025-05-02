from aiogram.fsm.state import StatesGroup, State


class Offer(StatesGroup):
    offer_index = State()