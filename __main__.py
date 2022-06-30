from aiogram import executor

from init_bot import InitBot
from deletion import PetDeletion
from adding import AddingPet
from searching import PetSearching
from editing import PetEditing

init_bot = InitBot()


def startup():
    PetDeletion()
    AddingPet()
    PetSearching()
    PetEditing()


if __name__ == '__main__':
    executor.start_polling(init_bot.dp, on_startup=startup())