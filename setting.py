import sqlalchemy
import psycopg2
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

db = 'postgresql://flores:zxc@localhost:5432/bot'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

token = ''
token_user = ""

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
