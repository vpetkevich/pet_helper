from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fields import fields

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


pet_menu = {
    'type': ReplyKeyboardMarkup(resize_keyboard=True).add('Кот', 'Собака', 'Другое', btn_cancel),
    'gender': ReplyKeyboardMarkup(resize_keyboard=True).add('Мальчик', 'Девочка', btn_cancel),
    'color': ReplyKeyboardMarkup(resize_keyboard=True).add('Белый', 'Черный', 'Рыжий', 'Трехцветный', 'Серый',
                                                               'Лесной', 'Смешанный', btn_cancel),
    'boolean': ReplyKeyboardMarkup(resize_keyboard=True).add('Да', 'Нет', btn_cancel),
    'breed': ReplyKeyboardMarkup(resize_keyboard=True).add('Без породы', btn_cancel),
    'district': ReplyKeyboardMarkup(resize_keyboard=True).add('Минская', 'Гомельская', 'Гродненская', 'Брестская',
                                                                  'Могилевская', btn_cancel),
    'description': ReplyKeyboardMarkup(resize_keyboard=True).add('Нет', btn_cancel),
    'photos': ReplyKeyboardMarkup(resize_keyboard=True).add('Все фотографии добавлены', btn_cancel)
}


class FieldsMenu:
    fields = [i for i in fields.keys()]
    fields_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
        'тип', 'имя', 'возраст', 'пол', 'окрас', 'вакцинирован(а)', 'обработан(а) от глистов/клещей', 'стерилизован(а)',
        'чипирован(а)', 'порода', 'город', 'область', 'номер телефона', 'дополнительная информация', btn_cancel)
