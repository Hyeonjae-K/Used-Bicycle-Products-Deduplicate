import time
import requests

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from usedproduct.models import Category, Product

USER_AGENT = {'User-Agent': 'Mozilla/5.0'}
JN_STORE = '중나'
BJ_STORE = '번장'


def extract_jn(item):
    url_prefix = 'https://m.cafe.naver.com/ca-fe/web/cafes/10050146/articles/%s'
    name = item['subject']
    price = item['cost']
    image = item['representImage']
    url = url_prefix % item['articleId']
    author = item['writerNickname']
    return {'name': name,
            'price': price,
            'image': image,
            'url': url,
            'author': author}


def extract_bj(item):
    url_prefix = 'https://m.bunjang.co.kr/products/%s'
    name = item['name']
    price = int(item['price']) if item['price'] != '연락요망' else 0
    image = item['product_image']
    url = url_prefix % item['pid']
    return {'name': name,
            'price': price,
            'image': image,
            'url': url,
            'author': None}


def extract_data(store, response):
    if store == JN_STORE:
        items = response.json()['message']['result']['articleList']
        return [extract_jn(item) for item in items]
    if store == BJ_STORE:
        items = response.json()['list']
        return [extract_bj(item) for item in items]


def crawl(category: Category):
    response = requests.get(category.url, USER_AGENT)
    return extract_data(category.store, response)


def save(category, items):
    new_products = [Product(name=item['name'],
                        price=item['price'],
                        image=item['image'],
                        url=item['url'],
                        author=item['author'],
                        category=category)
                for item in items
                if not Product.objects.filter(name=item['name'], price=item['price'])]
    Product.objects.bulk_create(new_products)


def run():
    categories = Category.objects.all()
    for category in categories:
        items = crawl(category)
        save(category, items)


if __name__ == '__main__':
    while True:
        try:
            run()
        except Exception as e:
            print(e)
        time.sleep(2)
