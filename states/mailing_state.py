from aiogram.dispatcher.filters.state import StatesGroup, State


class MailState(StatesGroup):
    message = State()