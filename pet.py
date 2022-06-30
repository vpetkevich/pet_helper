import uuid
from init_bot import InitBot

init_bot = InitBot()


class PhotoProcess:
    dir_created = False


class Pet:
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
        print(data_pet)

        query_pet_user = """INSERT INTO pet_user(pet_id, user_id) VALUES(?, ?)"""
        init_bot.curs.execute(query_pet, data_pet)
        data_pet_user = (pet_id, self.user_id)
        init_bot.curs.execute(query_pet_user, data_pet_user)

        init_bot.conn.commit()
