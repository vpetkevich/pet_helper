import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from init_bot import init_bot
from pet_states import deletion_states
import menus

pets_list = []


class DeletePet:
    @staticmethod
    async def display_pets(message: types.Message):
        await deletion_states.display.set()
        await message.reply("Кого из питомцев Вы хотите удалить?", reply_markup=menus.cancel_menu)
        user_id = message.from_user.id
        query_user_pet = f'SELECT pet_id FROM pet_user WHERE user_id = {user_id}'
        init_bot.curs.execute(query_user_pet)
        pets = init_bot.curs.fetchall()
        for i in pets:
            query_pet = f"SELECT id, name, photos FROM pet WHERE id = '{i[0]}'"
            init_bot.curs.execute(query_pet)
            pets_list.append(init_bot.curs.fetchall()[0])
        for i in pets_list:
            await init_bot.bot.send_message(chat_id=message.chat.id, text=f'Имя: {i[1]}')
            photos_dir = f'{os.getcwd()}/{i[2]}'
            for k in os.listdir(photos_dir):
                await init_bot.bot.send_photo(chat_id=message.chat.id, photo=open(f'{photos_dir}/{k}', 'rb'))
        await deletion_states.next()

    @staticmethod
    async def delete_pet(message: types.Message, state: FSMContext):
        pet_name = message.text
        if pet_name in [i[1] for i in pets_list]:
            for i in pets_list:
                if pet_name == i[1]:
                    query_pet = f'DELETE FROM pet WHERE id = "{i[0]}"'
                    query_pet_user = f'DELETE FROM pet_user WHERE pet_id = "{i[0]}"'
                    init_bot.curs.execute(query_pet)
                    init_bot.curs.execute(query_pet_user)
                    init_bot.conn.commit()
                    await init_bot.bot.send_message(chat_id=message.chat.id,
                                                    text=f'Питомец: "{i[1]}" успешно удален из каталога',
                                                    reply_markup=menus.main_menu)
                    await state.finish()
        else:
            await init_bot.bot.send_message(chat_id=message.chat.id,
                                            text="Питомца с таким именем нету, пожалуйста, "
                                            "перепроверьте и введите ещё раз",
                                            reply_markup=menus.main_menu)
            await state.finish()
