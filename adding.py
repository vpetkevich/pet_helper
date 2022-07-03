import aiogram.utils.markdown as md
import os
from aiogram import executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext

import menus
from fields import fields
from pet import Pet, init_bot
from pet_states import adding_states
from helpers import get_age


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

        await init_bot.bot.send_message(message.from_user.id, 'Укажите, пожалуйста, тип питомца',
                                        reply_markup=menus.pet_menu['type'])

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.type)
    async def process_type(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['тип']] = message.text

        await adding_states.next()
        await message.reply("Как питомца зовут?", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.name)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['имя']] = message.text

        await adding_states.next()
        await message.reply("Сколько питомцу лет/месяцев?", reply_markup=menus.cancel_menu)

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

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Мальчик", "Девочка"], state=adding_states.gender)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный пол, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.gender)
    async def process_gender(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['пол']] = message.text

        await adding_states.next()
        await message.reply("Окрас питомца?", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.color)
    async def process_color(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['окрас']] = message.text

        await adding_states.next()
        await message.reply("Наличие прививок?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.vaccinated)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.vaccinated)
    async def process_cured(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['вакцинирован(а)']] = message.text

        await adding_states.next()
        await message.reply("Обработан(а) от глистов/клещей?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.processed)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.processed)
    async def process_cured(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['обработан(а) от глистов/клещей']] = message.text

        await adding_states.next()
        await message.reply("Стерилизация?", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.sterilized)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.sterilized)
    async def process_cured(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['стерилизован(а)']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, чипирован ли питомец", reply_markup=menus.pet_menu['boolean'])

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.chip)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.chip)
    async def process_chip(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['чипирован(а)']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, породу питомца", reply_markup=menus.pet_menu['breed'])

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.breed)
    async def process_breed(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['порода']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, город", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.town)
    async def process_town(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['город']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, область", reply_markup=menus.pet_menu['district'])

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.district)
    async def process_district(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['область']] = message.text

        await adding_states.next()
        await message.reply("Укажите, пожалуйста, Ваш номер телефона", reply_markup=menus.cancel_menu)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.phone)
    async def process_phone(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[fields['номер телефона']] = message.text

        await adding_states.next()
        await message.reply("Загрузите, пожалуйста, фотографии питомца", reply_markup=menus.pet_menu['photos'])

    @staticmethod
    @init_bot.dp.message_handler(content_types="photo", state=adding_states.pictures)
    async def handle_docs_photo(message):
        Pet.photos_list_to_print.append(message.photo[3])

    @staticmethod
    @init_bot.dp.message_handler(text="Все фотографии добавлены", state=adding_states.pictures)
    async def photos_uploaded(message):
        await adding_states.next()
        await message.reply("Дополнительная информация?", reply_markup=menus.pet_menu['description'])

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.description)
    async def process_description(message: types.Message, state: FSMContext):
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

            pet = Pet(
                pet_type=data[fields["тип"]], name=data[fields["имя"]], age=data[fields["возраст"]],
                age_type=data['age_type'], rough_age=data['rough_age'], gender=data[fields["пол"]],
                color=data[fields["окрас"]], vaccinated=data[fields["вакцинирован(а)"]],
                processed=data[fields["обработан(а) от глистов/клещей"]], sterilized=data[fields["стерилизован(а)"]],
                chip=data[fields["чипирован(а)"]], breed=data[fields["порода"]], town=data[fields["город"]],
                district=data[fields["область"]], photos_dir=data['photos_dir'], phone=data[fields["номер телефона"]],
                description=data[fields["дополнительная информация"]], user_id=message.from_user.id)
            pet.write_to_db()

        await state.finish()
