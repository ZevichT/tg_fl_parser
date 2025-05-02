import asyncio
from json import JSONDecodeError

from bs4 import BeautifulSoup
import aiohttp
import json
from config import pages, parse_url

from database import OfferRepository

offers = []  # Список заказов
database_buffer = {}  # Список заказов, который будет добавлен в базу данных
idx = 0  # Индекс заказа. (P.S с enumerate не работает, ибо он скипает вакансии и происходит конфликт id-шников)

async def add_offer_to_db():
    for item in database_buffer:
        db_offer = database_buffer[f'{item}']
        await OfferRepository.add_offer(db_offer)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


try:
    with open('../cache.json', 'r', encoding='utf-8') as file:
        cache = json.load(file)
except (FileNotFoundError, JSONDecodeError):
    cache = {}

async def get_offer():
    global idx, database_buffer, offers

    async with aiohttp.ClientSession(headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }) as session:
        pages_tasks = []  # Список задач для загрузки страниц сайта

        for page in range(1, pages + 1):

            if page == 1:  # Если первая страница, то не меняем ссылку, ибо в другом исходе запросы зацикливаются
                url = f'{parse_url}'
            else:
                url = f'{parse_url}page-{page}'

            pages_tasks.append(asyncio.create_task(fetch(url, session)))
        pages_gather = await asyncio.gather(*pages_tasks)
        offers_params = []  # Список для параметров, которые в будущем передадутся в обработчик заказа
        for page_html in pages_gather:
            soup = BeautifulSoup(page_html, 'html.parser')
            offers_parse = soup.find_all('div', class_='b-post__grid')

            for data in offers_parse:
                offer = data.find('a',
                                  class_='text-dark text-decoration-none link-hover-danger cursor-pointer')  # Ищем название
                offer_url = offer['href']  # Ссылка на заказ
                if offer_url in cache:
                    cached_data = cache[offer_url]
                    offers.append([idx, cached_data['name'], cached_data['discreption'], cached_data['price'], offer_url])
                    idx += 1
                    continue  # Скипаем, если в кеше
                offers_params.append((idx, offer_url, offer.text))  # Добавляем в список параметров индекс, ссылку и название
                idx += 1

        offer_detail_tasks = []  # Список задач для асинхронной обработки целого заказа
        for index, url_offer, offer_name in offers_params:
            # Выглядит невероятно криво, но тут мы передаём параметры в функцию обработки полного заказа, создавая задачу исполнения этой функции
            offer_detail_tasks.append(asyncio.create_task(
            process_offer(session, index, url_offer, offer_name)))

        await asyncio.gather(*offer_detail_tasks)  # Выполняем асинхронную обработку заказов
async def process_offer(session, idx, url, name):
    global cache, offers, database_buffer
    offer_response = await fetch(f'https://www.fl.ru{url}', session)
    offer_soup = BeautifulSoup(offer_response, 'html.parser')

    offer_discreption = offer_soup.find_all('div', class_='text-5 b-layout__txt_padbot_20')  # Ищем описание
    discreption = ''
    for disc in offer_discreption:
        discreption += disc.text
    # Такой костыль был поставлен, т.к по неизвестной причине в описании заказ множество пустых строк. Мы их сплитим, затем объединяем.
    discreption = ' '.join(discreption.split())

    if discreption == '':  # Если заказ не имеет стандартного описания, то это вакансия и мы его скипаем
        return

    offer_price = offer_soup.find_all('div', class_='py-32 text-right unmobile flex-shrink-0 ml-auto mobile')  # Ищем цену
    price = ''
    for prices in offer_price:
        price += prices.text
    # Тот же костыль, что с описанием
    price = ' '.join(price.split())
    offers.append([idx, name, discreption, price, url])
    cache[url] = {  # Добавляем в кэш заказов
        'id': idx,
        'name': name,
        'discreption': discreption,
        'price': price
    }
    database_buffer[url] = { # Добавляем в кэш БД
        'name': name,
        'discreption': discreption,
        'price': price,
        'url': f'https://www.fl.ru{url}'
    }
asyncio.run(get_offer())
with open('../cache.json', 'w', encoding='utf-8') as file:
    json.dump(cache, file, ensure_ascii=False)
asyncio.run(add_offer_to_db())
offers = sorted(offers, key=lambda x: x[0])
