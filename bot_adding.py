from aiogram import executor, types
from aiogram.dispatcher import FSMContext

import menus
from init_bot import init_bot
from pet_states import adding_states
from py_adding import AddPet


class BotAdding:
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
        await AddPet().type(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.name)
    async def process_name(message: types.Message, state: FSMContext):
        await AddPet().name(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.age)
    async def process_age(message: types.Message, state: FSMContext):
        await AddPet().age(message, state)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Мальчик", "Девочка"], state=adding_states.gender)
    async def process_gender_invalid(message: types.Message):
        await message.reply("Неправильный пол, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.gender)
    async def process_gender(message: types.Message, state: FSMContext):
        await AddPet().gender(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.color)
    async def process_color(message: types.Message, state: FSMContext):
        await AddPet().color(message, state)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.vaccinated)
    async def process_vaccinated_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.vaccinated)
    async def process_vaccinated(message: types.Message, state: FSMContext):
        await AddPet().vaccinated(message, state)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.processed)
    async def process_processed_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.processed)
    async def process_processed(message: types.Message, state: FSMContext):
        await AddPet().processed(message, state)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.sterilized)
    async def process_sterilized_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.sterilized)
    async def process_sterilized(message: types.Message, state: FSMContext):
        await AddPet().sterilized(message, state)

    @staticmethod
    @init_bot.dp.message_handler(lambda message: message.text not in ["Да", "Нет"], state=adding_states.chip)
    async def process_chip_invalid(message: types.Message):
        await message.reply("Неправильный ответ, выберите, пожалуйста, из предложенных")

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.chip)
    async def process_chip(message: types.Message, state: FSMContext):
        await AddPet().chip(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.breed)
    async def process_breed(message: types.Message, state: FSMContext):
        await AddPet().breed(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.town)
    async def process_town(message: types.Message, state: FSMContext):
        await AddPet().town(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.district)
    async def process_district(message: types.Message, state: FSMContext):
        await AddPet().district(message, state)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.phone)
    async def process_phone(message: types.Message, state: FSMContext):
        await AddPet().phone(message, state)

    @staticmethod
    @init_bot.dp.message_handler(content_types="photo", state=adding_states.pictures)
    async def handle_docs_photo(message):
        await AddPet().photos(message)

    @staticmethod
    @init_bot.dp.message_handler(text="Все фотографии добавлены", state=adding_states.pictures)
    async def photos_uploaded(message):
        await AddPet().photos_uploaded(message)

    @staticmethod
    @init_bot.dp.message_handler(state=adding_states.description)
    async def process_description(message: types.Message, state: FSMContext):
        await AddPet().finalisation(message, state)