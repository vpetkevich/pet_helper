import unittest
from pet import Pet
import sqlite3


class PetsTest(unittest.TestCase):
    def test_adding(self):
        pet = Pet(
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
        a = curs.fetchall()
        self.assertEqual(a[0][2], 'Пушинка')


if __name__ == '__main__':
    unittest.main()
