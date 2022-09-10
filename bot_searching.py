from aiogram import types
from aiogram import executor
from aiogram.dispatcher import FSMContext

from init_bot import init_bot
from pet_states import searching_states
from py_searching import SearchPet


class PetSearching:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='Выбрать питомца')
    async def search_pets(message: types.Message):
        await SearchPet().search_pets(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.type)
    async def choose_type(message: types.Message):
        await SearchPet().choose_type(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.gender)
    async def choose_age(message: types.Message):
        await SearchPet().choose_age(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.color)
    async def choose_gender(message: types.Message):
        await SearchPet().choose_gender(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.district)
    async def choose_color(message: types.Message):
        await SearchPet().choose_color(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.town)
    async def choose_district(message: types.Message):
        await SearchPet().choose_district(message)

    @staticmethod
    @init_bot.dp.message_handler(state=searching_states.display)
    async def display_results(message: types.Message, state: FSMContext):
        await SearchPet().finalisation(message, state)
