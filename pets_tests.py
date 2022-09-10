import unittest
from aiogram import types, executor
from aiogram.dispatcher import FSMContext
from random import randint

from init_bot import init_bot
from py_adding import AddPet
from py_editing import EditPet
from py_searching import SearchPet
from py_deletion import DeletePet


class TestE2EPet:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='add_test', state='*')
    async def cmd_add_test(message: types.Message, state: FSMContext):
        msg = await init_bot.bot.send_message(message.from_user.id, 'Кот')
        await AddPet().type(msg, state)
        #pet_name = f'Котя{randint(0, 1000)}'
        #name for other tests
        pet_name = 'Котя'
        msg = await init_bot.bot.send_message(message.from_user.id, pet_name)
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

        query = f'SELECT * FROM pet WHERE name = "{pet_name}"'
        init_bot.curs.execute(query)
        assert init_bot.curs.fetchall()[0][2] == pet_name

    @staticmethod
    @init_bot.dp.message_handler(text='edit_test', state='*')
    async def cmd_edit_test(message: types.Message, state: FSMContext):
        query = f'UPDATE pet set gender = "Мальчик" where name = "Вася"'
        init_bot.curs.execute(query)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Вася')
        await EditPet().show_pets(msg)
        await EditPet().show_fields(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'пол')
        await EditPet().show_field_data(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Девочка')
        await EditPet().edit_field_data(msg, state)

        query = f'SELECT * FROM pet WHERE name = "Вася"'
        init_bot.curs.execute(query)
        assert init_bot.curs.fetchall()[0][6] == "Девочка"

    @staticmethod
    @init_bot.dp.message_handler(text='search_test', state='*')
    async def cmd_search_test(message: types.Message, state: FSMContext):
        await SearchPet().search_pets(message)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Кот')
        await SearchPet().choose_type(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'От 3 до 6')
        await SearchPet().choose_age(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Мальчик')
        await SearchPet().choose_gender(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Белый')
        await SearchPet().choose_color(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Минская')
        await SearchPet().choose_district(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Минск')
        await SearchPet().finalisation(msg, state)

    @staticmethod
    @init_bot.dp.message_handler(text='delete_test', state='*')
    async def cmd_search_test(message: types.Message, state: FSMContext):
        msg = await init_bot.bot.send_message(message.from_user.id, "Start")
        await DeletePet().display_pets(msg)
        msg = await init_bot.bot.send_message(message.from_user.id, "Котя582")
        await DeletePet().delete_pet(msg, state)



if __name__ == '__main__':
    unittest.main()
