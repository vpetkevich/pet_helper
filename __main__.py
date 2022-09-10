from aiogram import executor

from deletion import PetDeletion
from bot_adding import BotAdding
from searching import PetSearching
from bot_editing import PetEditing
from pets_tests import TestE2EPet
from init_bot import init_bot


def startup():
    PetDeletion()
    BotAdding()
    PetSearching()
    PetEditing()
    TestE2EPet()


if __name__ == '__main__':
    executor.start_polling(init_bot.dp, on_startup=startup())
