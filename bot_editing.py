from aiogram import types
from aiogram import executor
from aiogram.dispatcher import FSMContext

from init_bot import init_bot
from pet_states import editing_states
from py_editing import EditPet


class PetEditing:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='Редактировать питомца')
    async def display_pets(message: types.Message):
        await EditPet().show_pets(message)

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.fields_to_edit)
    async def show_fields(message: types.Message, state: FSMContext):
        await EditPet().show_fields(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.show_field_data)
    async def show_field_data(message: types.Message, state: FSMContext):
        await EditPet().show_field_data(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.edit_field)
    async def edit_field_data(message: types.Message, state: FSMContext):
        await EditPet().edit_field_data(message, state)

