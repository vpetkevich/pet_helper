import unittest
from pet import CreatePet, EditPet
import sqlite3


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


if __name__ == '__main__':
    unittest.main()
