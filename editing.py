import os
from aiogram import types
from aiogram import executor
from aiogram.dispatcher import FSMContext

from pet import init_bot, EditPet
from pet_states import editing_states
import menus
from fields import fields, bool_fields

pets_list = []


class PetEditing:
    def __init__(self):
        executor.start_polling(init_bot.dp)

    @staticmethod
    @init_bot.dp.message_handler(text='Редактировать питомца')
    async def display_pets(message: types.Message):
        await editing_states.display.set()
        await message.reply("Кого из питомцев Вы хотите отредактировать?", reply_markup=menus.cancel_menu)
        user_id = message.from_user.id
        query_user_pet = f'SELECT pet_id FROM pet_user WHERE user_id = {user_id}'
        init_bot.curs.execute(query_user_pet)
        pets = init_bot.curs.fetchall()
        for i in pets:
            query_pet = f"SELECT id, name, photos FROM pet WHERE id = '{i[0]}'"
            init_bot.curs.execute(query_pet)
            pets_list.clear()
            pets_list.append(init_bot.curs.fetchall()[0])
        for i in pets_list:
            await init_bot.bot.send_message(chat_id=message.chat.id, text=f'Имя: {i[1]}')
            photos_dir = f'{os.getcwd()}/{i[2]}'
            for k in os.listdir(photos_dir):
                await init_bot.bot.send_photo(chat_id=message.chat.id, photo=open(f'{photos_dir}/{k}', 'rb'))
        await editing_states.next()

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.fields_to_edit)
    async def show_fields(message: types.Message, state: FSMContext):
        await state.update_data(pet_name=message.text)
        if message.text in [i[1] for i in pets_list]:
            for i in pets_list:
                if message.text == i[1]:
                    await state.update_data(pet_id=i[0])
                    await init_bot.bot.send_message(chat_id=message.chat.id,
                                                    text='Выберите, пожалуйста, поле',
                                                    reply_markup=menus.FieldsMenu.fields_menu)
                    await editing_states.next()
        else:
            await init_bot.bot.send_message(chat_id=message.chat.id,
                                            text="Питомца с таким именем нету, пожалуйста, "
                                            "перепроверьте и попробуйте ещё раз",
                                            reply_markup=menus.main_menu)
            await state.finish()

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.show_field_data)
    async def show_field_data(message: types.Message, state: FSMContext):
        field_name = message.text
        await state.update_data(field_name=message.text)
        async with state.proxy() as data:
            query = f'SELECT {fields[field_name]} from pet where id="{data["pet_id"]}"'
            init_bot.curs.execute(query)
            field_data = init_bot.curs.fetchone()[0]
            markup = menus.cancel_menu
            if fields[field_name] in bool_fields:
                markup = menus.pet_menu['boolean']
                if field_data == 1:
                    field_data = 'Да'
                else:
                    field_data = 'Нет'
            elif fields[field_name] in menus.pet_menu:
                markup = menus.pet_menu[fields[field_name]]
            await message.reply(text=f'Текущее значение поля {field_name}: {field_data}', reply_markup=markup)
            await init_bot.bot.send_message(chat_id=message.chat.id, text='Введите новое значение:')
            await editing_states.next()

    @staticmethod
    @init_bot.dp.message_handler(state=editing_states.edit_field)
    async def edit_field_data(message: types.Message, state: FSMContext):
        edit_pet = EditPet()
        field_data_to_insert = message.text
        field_data_to_show = message.text
        async with state.proxy() as data:
            if fields[data['field_name']] in bool_fields:
                if field_data_to_insert == 'Да':
                    field_data_to_insert = 1
                else:
                    field_data_to_insert = 0
            edit_pet.edit_pet_field(fields[data['field_name']], field_data_to_insert, data['pet_id'])
            await message.reply(text=f'Новое значение поля {data["field_name"]}: {field_data_to_show}',
                                reply_markup=menus.main_menu)
            await state.finish()

    @staticmethod
    @init_bot.dp.message_handler(state='*', commands='Отмена')
    @init_bot.dp.message_handler(text='Отмена',  state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        await state.finish()
        await message.reply('Отменено.', reply_markup=menus.main_menu)
