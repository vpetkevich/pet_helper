from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import fields

btn_add_pet = KeyboardButton('Добавить питомца')
btn_find_pet = KeyboardButton('Выбрать питомца')
btn_edit_pet = KeyboardButton('Редактировать питомца')
btn_delete_post = KeyboardButton('Удалить запись')
btn_cancel = KeyboardButton('Отмена')
btn_optional_param = KeyboardButton('Не имеет значения')
btns_fields = [KeyboardButton(i) for i in fields.keys()]
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_pet, btn_delete_post, btn_edit_pet, btn_find_pet)
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)
search_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_optional_param, btn_cancel)


class FieldsMenu:
    btn_name = 'Имя'
    btn_type = 'Тип'
    btn_age = 'Возраст'
    btn_gender = 'Пол'
    btn_color = 'Окрас'
    btn_vaccinated = 'Вакцинация'
    btn_processed = 'Стерилизован(а)'
    btn_sterilized = 'Порода'
    btn_chip = 'Чип'
    btn_town = 'Город'
    btn_district = 'Область'
    btn_phone = 'Номер телефона'
    btn_description = 'Дополнительная информация'
    fields_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
        btn_name, btn_type, btn_age, btn_gender, btn_color, btn_vaccinated, btn_processed, btn_sterilized, btn_chip,
        btn_town, btn_district, btn_phone, btn_description, btn_cancel)
