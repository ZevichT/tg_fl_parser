from dotenv import load_dotenv
from os import getenv
from aiogram import Bot

load_dotenv()

bot = Bot(token=getenv('BOT'))  # Вставить свой api от бота
DB_URL = getenv('DB_URL')  # Вставить свою ссылку на базу данных
pages = 2  # Менять количество страниц для парсинга. Default - 2
parse_url = 'https://www.fl.ru/projects/category/programmirovanie/'