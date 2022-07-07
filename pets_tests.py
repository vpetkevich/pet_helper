import unittest
from aiogram import types, executor
from aiogram.dispatcher import FSMContext
from random import randint

from pet import init_bot
from py_adding import AddPet
from py_editing import EditPet


class TestE2EPet:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='add_test', state='*')
    async def cmd_add_test(message: types.Message, state: FSMContext):
        msg = await init_bot.bot.send_message(message.from_user.id, 'Кот')
        await AddPet().type(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, f'Котя{randint(0, 1000)}')
        await AddPet().name(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, '5 лет')
        await AddPet().age(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Мальчик')
        await AddPet().gender(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Белый')
        await AddPet().color(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Да')
        await AddPet().vaccinated(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Да')
        await AddPet().processed(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Нет')
        await AddPet().sterilized(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Нет')
        await AddPet().chip(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Без породы')
        await AddPet().breed(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Минск')
        await AddPet().town(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Минская')
        await AddPet().district(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, '81208102')
        await AddPet().phone(msg, state)
        msg = await init_bot.bot.send_photo(
            message.from_user.id,
            'AgACAgIAAxkBAAIoGWLGfomTNMR6YF05mSKq5DGVIqo5AAKbujEbHC8wSim3AAGaGjkz1gEAAwIAA3kAAykE')
        await AddPet().photos(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Все фотографии добавлены')
        await AddPet().photos_uploaded(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Нет')
        await AddPet().finalisation(msg, state)

    @staticmethod
    @init_bot.dp.message_handler(text='edit_test', state='*')
    async def cmd_edit_test(message: types.Message, state: FSMContext):
        msg = await init_bot.bot.send_message(message.from_user.id, 'Вася')
        await EditPet().show_pets(msg)
        await EditPet().show_fields(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'пол')
        await EditPet().show_field_data(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Девочка')
        await EditPet().edit_field_data(msg, state)






if __name__ == '__main__':
    unittest.main()
