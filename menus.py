from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fields import db_fields

btn_add_pet = KeyboardButton('Добавить питомца')
btn_find_pet = KeyboardButton('Выбрать питомца')
btn_edit_pet = KeyboardButton('Редактировать питомца')
btn_delete_post = KeyboardButton('Удалить запись')
btn_cancel = KeyboardButton('Отмена')
btn_optional_param = KeyboardButton('Не имеет значения')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_pet, btn_delete_post, btn_edit_pet, btn_find_pet)
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)
search_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_optional_param, btn_cancel)


pet_menu = {
    'type': ReplyKeyboardMarkup(resize_keyboard=True).add('Кот', 'Собака', 'Другое', btn_cancel),
    'gender': ReplyKeyboardMarkup(resize_keyboard=True).add('Мальчик', 'Девочка', btn_cancel),
    'color': ReplyKeyboardMarkup(resize_keyboard=True).add('Белый', 'Черный', 'Рыжий', 'Трехцветный', 'Серый',
                                                               'Лесной', 'Смешанный', btn_cancel),
    'boolean': ReplyKeyboardMarkup(resize_keyboard=True).add('Да', 'Нет', btn_cancel),
    'breed': ReplyKeyboardMarkup(resize_keyboard=True).add('Без породы', btn_cancel),
    'district': ReplyKeyboardMarkup(resize_keyboard=True).add('Минская', 'Гомельская', 'Гродненская', 'Брестская',
                                                                  'Могилевская'),
    'description': ReplyKeyboardMarkup(resize_keyboard=True).add('Нет', btn_cancel),
    'photos': ReplyKeyboardMarkup(resize_keyboard=True).add('Все фотографии добавлены', btn_cancel)
}


class FieldsMenu:
    fields_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
        db_fields['name'][1], db_fields['pet_type'][1], db_fields['age'][1], db_fields['gender'][1],
        db_fields['color'][1], db_fields['vaccinated'][1], db_fields['processed'][1], db_fields['sterilized'][1],
        db_fields['chip'][1], db_fields['town'][1], db_fields['district'][1], db_fields['phone'][1],
        db_fields['description'][1], btn_cancel)
