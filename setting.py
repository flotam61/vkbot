import sqlalchemy
import psycopg2
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

db = 'postgresql://flores:zxc@localhost:5432/bot'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

token = 'e439ee2f8ac14b6eed53eb7034a4ea911d6980016b1e9daa11bf256700d8f309dd1b2da5f07aa48e7e582'
token_user = "9a3e3d12366ac8a3ccfaf2ea00a060b14d2a6235ddb4e1134c22e0156b555f0d4cfb16fca109cc4b8700f"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
