from random import randrange
import requests
from setting import *

db = 'postgresql://flores:zxc@localhost:5432/bot'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

token = 'e439ee2f8ac14b6eed53eb7034a4ea911d6980016b1e9daa11bf256700d8f309dd1b2da5f07aa48e7e582'
token_user = "9a3e3d12366ac8a3ccfaf2ea00a060b14d2a6235ddb4e1134c22e0156b555f0d4cfb16fca109cc4b8700f"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            url = "https://api.vk.com/method/users.get"
            params = {"user_ids": event.user_id, "fields": 'bdate,city,relation,sex', "access_token": token, "v": "5.131"}
            resvk = requests.get(url, params=params).json()
            if 'relation' in resvk['response'][0]:
                relation = resvk['response'][0]['relation']
            else:
                relation = 0

            test_have_id = connection.execute("""SELECT id_vk FROM vkbot
            WHERE id_vk = %s;""", (event.user_id)).fetchone()
            print(resvk)

            if request == "привет" or request == "Привет":
                if test_have_id == None:
                    write_msg(event.user_id, f"Начинаем регистрацию")
                    if 'city' in resvk['response'][0]:
                        city = resvk['response'][0]['city']['title']
                        cityid = resvk['response'][0]['city']['id']
                    else:
                        write_msg(event.user_id, f"Твой город мне неизвестен. Введите название вашего города")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                city = event.text
                                break
                    if 'bdate' in resvk['response'][0]:
                        if len(resvk['response'][0]['bdate']) > 6:
                            age = 2022 - int(resvk['response'][0]['bdate'][-4:])
                            # думаю точный возраст необязательно
                        elif len(resvk['response'][0]['bdate']) < 5:
                            write_msg(event.user_id, f"Не понимаю сколько вам лет, введите вручную")
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                    age = int(event.text)
                                    break
                    else:
                        write_msg(event.user_id, f"Не понимаю сколько вам лет, введите вручную")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                age = int(event.text)
                                break

                    connection.execute("""INSERT INTO vkbot(id_vk, first_name, last_name, sex, city_name, age_user, relation) VALUES(%s, %s, %s, %s, %s, %s, %s);""",
                    (event.user_id, resvk['response'][0]['first_name'], resvk['response'][0]['last_name'], resvk['response'][0]['sex'], city, age, relation))
                    write_msg(event.user_id, f'Регистрация завершена')

                elif test_have_id != None:
                    write_msg(event.user_id, f"Привет, {resvk['response'][0]['first_name']}!")

            elif request == "Информация" or request == "информация" or request == "инфа":
                information_user_bd = connection.execute("""SELECT first_name, last_name, city_name, age_user FROM vkbot
                            WHERE id_vk = %s;""", (event.user_id)).fetchall()
                for x in information_user_bd:
                    write_msg(event.user_id, f'Информация о вас: {x}')

            elif request == "Поиск" or request == "поиск":
                name_user_bd = connection.execute("""SELECT first_name FROM vkbot
                            WHERE id_vk = %s;""", (event.user_id)).fetchone()
                for name_user_bd_in in name_user_bd:
                    write_msg(event.user_id, f'Сейчас начнём поиск, {name_user_bd_in}')

                sex_user = connection.execute("""SELECT sex FROM vkbot
                WHERE id_vk = %s;""", (event.user_id)).fetchone()
                for sex_user_in in sex_user:
                    print()

                city_user = connection.execute("""SELECT city_name FROM vkbot
                WHERE id_vk = %s;""", (event.user_id)).fetchone()
                for city_user_in in city_user:
                    print()

                age_user = connection.execute("""SELECT age_user FROM vkbot
                WHERE id_vk = %s;""", (event.user_id)).fetchone()
                for age_user_in in age_user:
                    print()

                if sex_user_in == 2:
                    sex_user_vs = 1
                elif sex_user_in == 1:
                    sex_user_vs = 2
                url = "https://api.vk.com/method/users.search"
                params = {"hometown": city_user_in, "age_from": age_user_in - 2, "age_to": age_user_in + 2, "count": "5", "sex": sex_user_vs, "access_token": token_user, "v": "5.131"}
                newdata = requests.get(url, params=params).json()
                for q in newdata['response']['items']:
                    write_msg(event.user_id, f"{q['first_name']} {q['last_name']} - https://vk.com/id{q['id']}")
            else:
                write_msg(event.user_id, f'Для регистрации напишите "Привет".\n Чтобы искать пару, напишите "Поиск".'
                                         f'\n Введите "Информация" чтобы проверить информацию о себе.')