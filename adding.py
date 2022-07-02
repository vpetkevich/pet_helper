import aiogram.utils.markdown as md
import os
from aiogram import executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext

import menus
from config import fields
from pet import Pet, init_bot, PhotoProcess
from pet_states import adding_states
from helpers import get_age

photo_process = PhotoProcess()


class AddingPet:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        await init_bot.bot.send_message(message.from_user.id, 'Привет, {0.first_name}'.format(message.from_user),
                                        reply_markup=menus.main_menu)

    @staticmethod
    @init_bot.dp.message_handler(state='*', commands='Отмена')
    @init_bot.dp.message_handler(text='Отмена',  state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        await state.finish()
        await message.reply('Отменено.', reply_markup=menus.main_menu)

    @staticmethod
    @init_bot.dp.message_handler(text="Добавить питомца")
    async def add_pet(message: types.Message):
        await adding_states.type.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Кот", "Собака", "Другое", "Отмена")
        await init_bot.bot.send_message(message.from_user.id, 'Укажите, пожалуйста, тип питомца', reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.type)
    async def process_type(message: types.Message, state: FSMContext):
        await state.update_data(pet_type=message.text)

        await adding_states.next()
        await message.reply("Как питомца зовут?", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.name)
    async def process_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)

        await adding_states.next()
        await message.reply("Сколько питомцу лет/месяцев?")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.age)
    async def process_age(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            a = True
            for i in ['лет', 'года', 'месяца', 'месяцев', 'месяц', 'год']:
                if message.text.find(i) != -1:
                    data['age_type'] = i
                    a = False
                    if 'месяц' in message.text:
                        for k in ['лет', 'год']:
                            if message.text.find(k):
                                data['age'] = get_age(message.text)
                            else:
                                data['age'] = 0
                    else:
                        data['age'] = get_age(message.text)
                    data['rough_age'] = message.text
                    break
            if a:
                await message.reply("Некорректный возраст, введите, "
                                    "пожалуйста по одному из примеров: \n2 месяца \n2 года \n2 года и 2 месяца")
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add("Мальчик", "Девочка", "Отмена")
                await message.reply("Пол питомца?", reply_markup=markup)
                await adding_states.next()

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Мальчик", "Девочка"], state=adding_states.gender)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный пол, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.gender)
    async def process_gender(message: types.Message, state: FSMContext):
        await state.update_data(gender=message.text)
        await adding_states.next()
        await message.reply("Окрас питомца?", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.color)
    async def process_color(message: types.Message, state: FSMContext):
        await adding_states.next()
        await state.update_data(color=message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Да", "Нет", "Отмена")
        await message.reply("Наличие прививок?", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.vaccinated)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.vaccinated)
    async def process_cured(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['vaccinated'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Да", "Нет", "Отмена")
        await message.reply("Обработан(а) от глистов/клещей?", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.processed)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.processed)
    async def process_cured(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['processed'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Да", "Нет", "Отмена")
        await message.reply("Стерилизация?", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.sterilized)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.sterilized)
    async def process_cured(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['sterilized'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Да", "Нет", "Отмена")

        await message.reply("Укажите, пожалуйста, чипирован ли питомец", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.chip)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.chip)
    async def process_chip(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['chip'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Без породы", "Отмена")
        await message.reply("Укажите, пожалуйста, породу питомца", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.breed)
    async def process_breed(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['breed'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Отмена")

        await message.reply("Укажите, пожалуйста, город", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.town)
    async def process_town(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['town'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Отмена")

        await message.reply("Укажите, пожалуйста, область", reply_markup=markup)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.district)
    async def process_district(message: types.Message, state: FSMContext):
        await adding_states.next()
        async with state.proxy() as data:
            data['district'] = message.text

        await message.reply("Укажите, пожалуйста, Ваш номер телефона")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.phone)
    async def process_phone(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['phone'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Все фотографии добавлены", "Отмена")

        await message.reply("Загрузите, пожалуйста, фотографии питомца", reply_markup=markup)
        await adding_states.next()

    @staticmethod
    @init_bot.dp.message_handler(content_types="photo", state=adding_states.pictures)
    async def handle_docs_photo(message):
        Pet.photos_list_to_print.append(message.photo[3])

    @staticmethod
    @init_bot.dp.message_handler(text="Все фотографии добавлены", state=adding_states.pictures)
    async def photos_uploaded(message, state: FSMContext):
        await adding_states.next()
        await message.reply("Дополнительная информация?", reply_markup=menus.cancel_menu)
        await state.update_data(has_folder=1)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.description)
    async def process_description(message: types.Message, state: FSMContext):
        await adding_states.next()
        await state.update_data(description=message.text)

        async with state.proxy() as data:
            data['description'] = message.text

            await init_bot.bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Проверьте, пожалуйста, всё ли правильно.'),
                    md.bold('Имя:', data[f'{fields["Имя"]}']),
                    md.text('Тип:', data[f'{fields["Тип"]}']),
                    md.text('Возраст:', data[f'{fields["Возраст"]}']),
                    md.text('Пол:', data[f'{fields["Пол"]}']),
                    md.text('Окрас:', data[f'{fields["Окрас"]}']),
                    md.text('Вакцинация:', data[f'{fields["Вакцинация"]}']),
                    md.text('Обработан(а) от глистов/клещей:', data[f'{fields["Обработан(а) от глистов/клещей"]}']),
                    md.text('Стерилизован(а):', data[f'{fields["Стерилизован(а)"]}']),
                    md.text('Чипирован(а):', data[f'{fields["Чипирован(а)"]}']),
                    md.text('Порода:', data[f'{fields["Порода"]}']),
                    md.text('Город:', data[f'{fields["Город"]}']),
                    md.text('Область:', data[f'{fields["Область"]}']),
                    md.text('Номер телефона:', data[f'{fields["Номер телефона"]}']),
                    md.text('Дополнительная информация:', data[f'{fields["Дополнительная информация"]}']),
                    sep='\n',
                ),
                reply_markup=menus.main_menu,
                parse_mode=ParseMode.MARKDOWN,
            )
            data['photos_dir'] = f'pictures/{message.message_id} {message.chat.id}'
            for i in Pet.photos_list_to_print:
                try:
                    os.mkdir(data['photos_dir'])
                except FileNotFoundError:
                    os.mkdir('pictures')
                    os.mkdir(f'pictures/{message.message_id} {message.chat.id}')
                    pass
                await init_bot.bot.download_file_by_id(
                    file_id=i.file_id, destination=f'pictures/{message.message_id} {message.chat.id}/{i.file_id}.jpeg')
                await init_bot.bot.send_photo(message.chat.id, i.file_id)
            Pet.photos_list_to_print.clear()

            pet = Pet(pet_type=data['pet_type'], name=data['name'], age=data['age'], age_type=data['age_type'],
                      rough_age=data['rough_age'], gender=data['gender'], color=data['color'],
                      vaccinated=data['vaccinated'], processed=data['processed'], sterilized=data['sterilized'],
                      chip=data['chip'], breed=data['breed'], town=data['town'], district=data['district'],
                      photos_dir=data['photos_dir'], phone=data['phone'], description=data['description'],
                      user_id=message.from_user.id)
            pet.write_to_db()

        await state.finish()
