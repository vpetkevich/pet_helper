from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from init_bot import init_bot
from pet_states import deletion_states
from py_deletion import DeletePet


class PetDeletion:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='Удалить запись')
    async def display_pets(message: types.Message):
        await DeletePet().display_pets(message)

    @staticmethod
    @init_bot.dp.message_handler(state=deletion_states.delete)
    async def delete_pets(message: types.Message, state: FSMContext):
        await DeletePet().delete_pet(message, state)
