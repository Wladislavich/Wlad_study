# Задача:
# Источник данных https://5ka.ru/special_offers/
# Необходимо создать структуру JSON файлов где имя файла название категории, а содержимое файла JSON список
# словарей товаров, принадлежащих этой категории.
# Извлекаем только товары по акции, не перегружайте сервер делайте time.sleep
# В Гите хранить файлы результата не нужно, только код который приводит к созданию соответствующих файлов

import requests
import json
import time
import re

url = 'https://5ka.ru/api/v2/special_offers/'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.4.143 Yowser/2.5 Yptp/1.56 Safari/537.36'}
cat_url = 'https://5ka.ru/api/v2/categories/'

categories_response =requests.get(cat_url, headers=headers)
categories_json =json.loads(categories_response.text)
reg = re.compile('[^a-zA-Zа-яА-я1-90!? ]')
categories = dict()
for cat in categories_json:
    categories[cat['parent_group_code']] = reg.sub('', cat['parent_group_name'])

def goods_pack(url, params, category):
    result = []
    while url:
        response = requests.get(url, headers=headers, params=params) if params else requests.get(url, headers=headers)
        params = None
        data = response.json()
        result.extend(data.get('results'))
        url = data.get('next')
        time.sleep(1)
    with open(category + '.json', 'w') as file:
        file.write(json.dumps(data))
    return result

for category in categories.keys():
    params = {'categories':category}
    goods_pack(url, params, categories[category])