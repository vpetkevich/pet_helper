from aiogram.dispatcher.filters.state import State, StatesGroup


class AddingStates(StatesGroup):
    type = State()
    name = State()
    age = State()
    gender = State()
    color = State()
    vaccinated = State()
    processed = State()
    sterilized = State()
    chip = State()
    breed = State()
    town = State()
    district = State()
    phone = State()
    pictures = State()
    description = State()


adding_states = AddingStates()


class DeletionStates(StatesGroup):
    display = State()
    delete = State()


deletion_states = DeletionStates()


class EditingStates(StatesGroup):
    display = State()
    fields_to_edit = State()
    show_field_data = State()
    edit_field = State()


editing_states = EditingStates()


class SearchingStates(StatesGroup):
    params = State()
    type = State()
    gender = State()
    color = State()
    district = State()
    town = State()
    display = State()


searching_states = SearchingStates()
