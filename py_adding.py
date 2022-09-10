from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
import os
from aiogram.types import ParseMode
import uuid

from fields import fields
from init_bot import init_bot
from pet_states import adding_states
import menus
from helpers import get_age


class AddPet:
    @staticmethod
    async def type(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['тип']] = message.text
        await adding_states.next()
        await message.reply("Как питомца зовут?", reply_markup=menus.cancel_menu)

    @staticmethod
    async def name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['имя']] = message.text

        await adding_states.next()
        await message.reply("Сколько питомцу лет/месяцев?", reply_markup=menus.cancel_menu)

    @staticmethod
    async def age(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            a = True
            for i in ['лет', 'года', 'месяца', 'месяцев', 'месяц', 'год']:
                if message.text.find(i) != -1:
                    data['age_type'] = i
                    a = False
                    if 'месяц' in message.text:
                        for k in ['лет', 'год']:
                            if message.text.find(k):
                                data[fields['возраст']] = get_age(message.text)
                            else:
                                data[fields['возраст']] = 0
                    else:
                        data[fields['возраст']] = get_age(message.text)
                    data['rough_age'] = message.text
                    break
            if a:
                await message.reply("Некорректный возраст, введите, "
                                    "пожалуйста по одному из примеров: \n2 месяца \n2 года \n2 года и 2 месяца")
            else:
                await adding_states.next()
                await message.reply("Пол питомца?", reply_markup=menus.pet_menu['gender'])
            print(data[fields['возраст']])

    @staticmethod
    async def gender(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['пол']] = message.text

        await adding_states.next()
        await message.reply("Окрас питомца?", reply_markup=menus.cancel_menu)

    @staticmethod
    async def color(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['окрас']] = message.text

        await adding_states.next()
        await message.reply("Наличие прививок?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    async def vaccinated(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['вакцинирован(а)']] = message.text

        await adding_states.next()
        await message.reply("Обработан(а) от глистов/клещей?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    async def processed(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['обработан(а) от глистов/клещей']] = message.text

        await adding_states.next()
        await message.reply("Стерилизация?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    async def sterilized(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['стерилизован(а)']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, чипирован ли питомец", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    async def chip(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['чипирован(а)']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, породу питомца", reply_markup=menus.pet_menu['breed'])

    @staticmethod
    async def breed(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['порода']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, город", reply_markup=menus.cancel_menu)

    @staticmethod
    async def town(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['город']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, область", reply_markup=menus.pet_menu['district'])

    @staticmethod
    async def district(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['область']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, Ваш номер телефона", reply_markup=menus.cancel_menu)

    @staticmethod
    async def phone(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['номер телефона']] = message.text

        await adding_states.next()
        await message.reply("Загрузите, пожалуйста, фотографии питомца", reply_markup=menus.pet_menu['photos'])

    @staticmethod
    async def photos(message: types.Message):
        CreatePetRow.photos_list_to_print.append(message.photo[3])

    @staticmethod
    async def photos_uploaded(message: types.Message):
        await adding_states.next()
        await message.reply("Дополнительная информация?", reply_markup=menus.pet_menu['description'])

    @staticmethod
    async def finalisation(message: types.Message, state: FSMContext):
        await adding_states.next()
        await state.update_data(description=message.text)

        async with state.proxy() as data:
            data[fields['дополнительная информация']] = message.text

            await init_bot.bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Проверьте, пожалуйста, всё ли правильно.'),
                    md.bold(f'Имя:', data[f'{fields["имя"]}']),
                    md.text(f'Тип:', data[f'{fields["тип"]}']),
                    md.text(f'Возраст:', data[f'{fields["возраст"]}']),
                    md.text(f'Пол:', data[f'{fields["пол"]}']),
                    md.text(f'Цвет:', data[f'{fields["окрас"]}']),
                    md.text(f'Вакцинирован(а):', data[f'{fields["вакцинирован(а)"]}']),
                    md.text(f'Обработан(а) от глистов/клещей:', data[f'{fields["обработан(а) от глистов/клещей"]}']),
                    md.text(f'Стерилизован(а):', data[f'{fields["стерилизован(а)"]}']),
                    md.text(f'Чипирован(а):', data[f'{fields["чипирован(а)"]}']),
                    md.text(f'Порода:', data[f'{fields["порода"]}']),
                    md.text(f'Город:', data[f'{fields["город"]}']),
                    md.text(f'Область:', data[f'{fields["область"]}']),
                    md.text(f'Номер телефона:', data[f'{fields["номер телефона"]}']),
                    md.text(f'Дополнительная информация:', data[f'{fields["дополнительная информация"]}']),
                    sep='\n',
                ),
                reply_markup=menus.main_menu,
                parse_mode=ParseMode.MARKDOWN,
            )
            data['photos_dir'] = f'pictures/{message.message_id} {message.chat.id}'
            for i in CreatePetRow.photos_list_to_print:
                try:
                    os.mkdir(data['photos_dir'])
                except FileNotFoundError:
                    os.mkdir('pictures')
                    os.mkdir(f'pictures/{message.message_id} {message.chat.id}')
                    pass
                await init_bot.bot.download_file_by_id(
                    file_id=i.file_id, destination=f'pictures/{message.message_id} {message.chat.id}/{i.file_id}.jpeg')
                await init_bot.bot.send_photo(message.chat.id, i.file_id)
                print(i.file_id)
            CreatePetRow.photos_list_to_print.clear()

            pet = CreatePetRow(
                pet_type=data[fields["тип"]], name=data[fields["имя"]], age=data[fields["возраст"]],
                age_type=data['age_type'], rough_age=data['rough_age'], gender=data[fields["пол"]],
                color=data[fields["окрас"]], vaccinated=data[fields["вакцинирован(а)"]],
                processed=data[fields["обработан(а) от глистов/клещей"]], sterilized=data[fields["стерилизован(а)"]],
                chip=data[fields["чипирован(а)"]], breed=data[fields["порода"]], town=data[fields["город"]],
                district=data[fields["область"]], photos_dir=data['photos_dir'], phone=data[fields["номер телефона"]],
                description=data[fields["дополнительная информация"]], user_id=message.from_user.id)
            pet.write_to_db()

        await state.finish()


class CreatePetRow:
    def __init__(self, pet_type, name, age, age_type, rough_age, gender, color, vaccinated, processed, sterilized, chip,
                 breed, town, district, photos_dir, phone, description, user_id):
        self.pet_type = pet_type
        self.name = name
        self.age = age
        self.age_type = age_type
        self.rough_age = rough_age
        self.gender = gender
        self.color = color
        self.breed = breed
        self.town = town
        self.district = district
        self.photos_dir = photos_dir
        self.phone = phone
        self.description = description
        self.user_id = user_id

        self.bool_list = [vaccinated, processed, sterilized, chip]
        for i in self.bool_list:
            if i == 'Да':
                self.bool_list[self.bool_list.index(i)] = True
            else:
                self.bool_list[self.bool_list.index(i)] = False

    photos_list_to_print = []

    def write_to_db(self):
        query_pet = """INSERT INTO pet(id, pet_type, name, age, age_type, rough_age, gender, color, vaccinated,
        processed, sterilized, chip, breed, town, district, phone, photos, description)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        pet_id = str(uuid.uuid1())
        data_pet = (pet_id, self.pet_type, self.name, self.age, self.age_type, self.rough_age, self.gender, self.color,
                    self.bool_list[0], self.bool_list[1], self.bool_list[2], self.bool_list[3], self.breed, self.town,
                    self.district, self.phone, self.photos_dir, self.description)

        query_pet_user = """INSERT INTO pet_user(pet_id, user_id) VALUES(?, ?)"""
        init_bot.curs.execute(query_pet, data_pet)
        data_pet_user = (pet_id, self.user_id)
        init_bot.curs.execute(query_pet_user, data_pet_user)

        init_bot.conn.commit()

