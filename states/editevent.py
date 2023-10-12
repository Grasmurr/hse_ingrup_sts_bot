from aiogram.dispatcher.filters.state import StatesGroup, State


class EditEventState(StatesGroup):
    edit_event = State()
    delete_event = State()
    final_delete = State()


class AddEventState(StatesGroup):
    name_of_event = State()
    cost_of_event = State()
    description_of_event = State()
    event_photo = State()
    finish_adding = State()
