import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
import os

from init_bot import init_bot
from pet_states import searching_states
import menus
from aiogram.types import ReplyKeyboardMarkup


class SearchPet:
    pet_data = {}

    @staticmethod
    async def search_pets(message: types.Message):
        await searching_states.params.set()
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add("Кот", "Собака", "Другое", menus.btn_optional_param,
                                                             menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Давайте подберём питомца по параметрам",
                                        reply_markup=menu)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Тип")
        await searching_states.next()

    async def choose_type(self, message: types.Message):
        self.pet_data['pet_type'] = message.text

        menu = ReplyKeyboardMarkup(resize_keyboard=True).add("До года", "От 1 до 3", "От 3 до 6",
                                                             menus.btn_optional_param, menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Возраст", reply_markup=menu)
        await searching_states.next()

    async def choose_age(self, message: types.Message):
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add("Мальчик", "Девочка", menus.btn_optional_param,
                                                             menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Пол", reply_markup=menu)
        if message.text != 'Не имеет значения':
            if message.text == "До года":
                self.pet_data['age'] = 0
            elif message.text == "От 1 до 3":
                self.pet_data['age'] = 1, 2,
            else:
                self.pet_data['age'] = 3, 4, 5,
        await searching_states.next()

    async def choose_gender(self, message: types.Message):
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add("Белый", "Черный", "Рыжий", "Трехцветный", "Серый",
                                                             "Лесной", "Смешанный", menus.btn_optional_param,
                                                             menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Окрас", reply_markup=menu)
        if message.text != 'Не имеет значения':
            self.pet_data['gender'] = message.text
        await searching_states.next()

    async def choose_color(self, message: types.Message):
        if message.text != 'Не имеет значения':
            self.pet_data['color'] = message.text
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
            "Минская", "Гомельская", "Гродненская", "Витебская", "Брестская",
            menus.btn_optional_param, menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Область", reply_markup=menu)
        await searching_states.next()

    async def choose_district(self, message: types.Message):
        if message.text != 'Не имеет значения':
            self.pet_data['district'] = message.text
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add(menus.btn_optional_param, menus.btn_cancel)
        await init_bot.bot.send_message(chat_id=message.chat.id, text="Город", reply_markup=menu)
        await searching_states.next()

    async def finalisation(self, message: types.Message, state: FSMContext):
        if message.text != 'Не имеет значения':
            self.pet_data['town'] = message.text
        if self.pet_data != {}:
            where_clause = 'SELECT * FROM pet WHERE'
            n = 0
            for i, j in self.pet_data.items():
                if type(j) == tuple:
                    if n == 0:
                        where_clause = f'{where_clause} {i} in {j}'
                    else:
                        where_clause = f'{where_clause} and {i} in {j}'
                    n += 1
                else:
                    if n == 0:
                        where_clause = f'{where_clause} {i} in ("{j}")'
                    else:
                        where_clause = f'{where_clause} and {i} in ("{j}")'
                    n += 1
            print(where_clause)
        else:
            where_clause = 'SELECT * FROM pet'
        init_bot.curs.execute(where_clause)
        pets = init_bot.curs.fetchall()
        parsed_pet_data = {'Имя': '', 'Тип': '', 'Возраст': '', 'Пол': '', 'Окрас': '', 'Вакцинация': '',
                           'Обработан(а) от глистов/клещей': '', 'Стерилизован(а)': '', 'Чип': '', 'Порода': '',
                           'Город': '', 'Область': '', 'Номер телефона': '', 'Дополнительная информация': ''}
        if pets:
            for i in pets:
                parsed_pet_data['Тип'] = i[1]
                parsed_pet_data['Имя'] = i[2]
                parsed_pet_data['Возраст'] = i[5]
                parsed_pet_data['Пол'] = i[6]
                parsed_pet_data['Окрас'] = i[7]
                if i[8] == 1:
                    parsed_pet_data['Вакцинация'] = 'Да'
                else:
                    parsed_pet_data['Вакцинация'] = 'Нет'
                if i[9] == 1:
                    parsed_pet_data['Обработан(а) от глистов/клещей'] = 'Да'
                else:
                    parsed_pet_data['Обработан(а) от глистов/клещей'] = 'Нет'
                if i[10] == 1:
                    parsed_pet_data['Стерилизован(а)'] = 'Да'
                else:
                    parsed_pet_data['Стерилизован(а)'] = 'Нет'
                if i[11] == 1:
                    parsed_pet_data['Чипирован(а)'] = 'Да'
                else:
                    parsed_pet_data['Чипирован(а)'] = 'Нет'
                parsed_pet_data['Порода'] = i[12]
                parsed_pet_data['Город'] = i[13]
                parsed_pet_data['Область'] = i[14]
                parsed_pet_data['Номер телефона'] = i[15]
                parsed_pet_data['Дополнительная информация'] = i[17]
                a = await init_bot.bot.send_message(
                    message.chat.id,
                    md.text(
                        md.text('Имя:', parsed_pet_data['Имя']),
                        md.text('Тип:', parsed_pet_data['Тип']),
                        md.text('Возраст:', parsed_pet_data['Возраст']),
                        md.text('Пол:', parsed_pet_data['Пол']),
                        md.text('Окрас:', parsed_pet_data['Окрас']),
                        md.text('Вакцинация:', parsed_pet_data['Вакцинация']),
                        md.text('Обработан(а) от глистов/клещей:', parsed_pet_data['Обработан(а) от глистов/клещей']),
                        md.text('Стерилизован(а):', parsed_pet_data['Стерилизован(а)']),
                        md.text('Чипирован(а):', parsed_pet_data['Чипирован(а)']),
                        md.text('Порода:', parsed_pet_data['Порода']),
                        md.text('Город:', parsed_pet_data['Город']),
                        md.text('Область:', parsed_pet_data['Область']),
                        md.text('Номер телефона:', parsed_pet_data['Номер телефона']),
                        md.text('Дополнительная информация:', parsed_pet_data['Дополнительная информация']),
                        sep='\n',
                    ),
                    reply_markup=menus.main_menu,
                )
                for k in os.listdir(i[16]):
                    await init_bot.bot.send_photo(chat_id=message.chat.id, photo=open(f'{i[16]}/{k}', 'rb'),
                                                  reply_to_message_id=a.message_id)
            self.pet_data.clear()
        else:
            await init_bot.bot.send_message(
                message.chat.id,
                text='Не найдено',
                reply_markup=menus.main_menu
            )
        await state.finish()