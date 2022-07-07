import unittest
import sqlite3
from aiogram import types, executor
from aiogram.dispatcher import FSMContext

from pet import CreatePet, EditPet, init_bot
from py_adding import AddPet


class PetsTest(unittest.TestCase):
    def test_adding(self):
        pet = CreatePet(
            pet_type="Кот", name="Пушинка", age="3 года",
            age_type="года", rough_age="3 года", gender="Мальчик",
            color="Белый", vaccinated="Да",
            processed="Да", sterilized="Да",
            chip="Да", breed="Без породы", town="Минск",
            district="Минская", photos_dir="pictures/9887 460795077", phone="1231231123",
            description="Нет", user_id="6c185a0e-faca-11ec-ab67-acde48001122")
        pet.write_to_db()

        conn = sqlite3.connect('pet_helper.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM pet where name='Пушинка'")
        pet_name = curs.fetchall()[0][2]
        self.assertEqual(pet_name, 'Пушинка')

    def test_editing(self):
        edit_pet = EditPet()
        conn = sqlite3.connect('pet_helper.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM pet where name='Пушинка'")
        pet_id = curs.fetchall()[0][0]

        edit_pet.edit_pet_field("color", "Черный", pet_id)

        curs.execute("SELECT * FROM pet where name='Пушинка'")
        pet_color = curs.fetchall()[0][7]
        self.assertEqual(pet_color, "Черный")


class TestE2EPet:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='add_test', state='*')
    async def cmd_test(message: types.Message, state: FSMContext):
        msg = await init_bot.bot.send_message(message.from_user.id, 'Кот')
        await AddPet().type(msg, state)
        msg = await init_bot.bot.send_message(message.from_user.id, 'Вася')
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







if __name__ == '__main__':
    unittest.main()
