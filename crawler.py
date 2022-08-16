import time
import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from products.models import Product

products = Product.objects.all()


def parse_jg(data):
    url_prefix = 'https://m.cafe.naver.com/ca-fe/web/cafes/10050146/articles/%d'
    new_products = []

    for json in data:
        if json['type'] != 'ARTICLE':
            continue
        item = json['item']
        title = item['subject']
        author = item['writerNickname']
        price = item['cost']
        url = url_prefix % item['articleId']
        src = item['representImage'] if 'representImage' in item.keys() else None

        if not products.filter(title=title, author=author):
            new_products.append(
                Product(title=title, author=author, price=price, src=src, url=url, market='중나'))

    return new_products


def parse_bj(data):
    url_prefix = 'https://m.bunjang.co.kr/products/%s'
    new_products = []

    for item in data:
        title = item['name']
        price = int(item['price']) if item['price'] != '연락요망' else 0
        url = url_prefix % item['pid']
        src = item['product_image']

        if not products.filter(url=url):
            new_products.append(
                Product(title=title, price=price, url=url, src=src, market='번장'))

    return new_products


def crawl():
    new_products = []

    # jg
    jg_url = 'https://apis.naver.com/cafe-web/cafe2/ArticleList.json?search.clubid=10050146&search.queryType=lastArticle&search.menuid=432&search.page=1&search.perPage=50&ad=true&uuid=a04329ff-ffe2-4292-9bd6-45c98d9cc0e4&adUnit=MW_CAFE_ARTICLE_LIST_RS'
    data = requests.get(jg_url).json()['message']['result']['articleList']
    new_products.extend(parse_jg(data))

    # bj
    bj_url = 'https://api.bunjang.co.kr/api/1/find_v2.json?f_category_id=700350500&page=0&order=date&req_ref=category&request_id=2022814161912&stat_device=w&n=100&version=4'
    data = requests.get(bj_url).json()['list']
    new_products.extend(parse_bj(data))

    Product.objects.bulk_create(new_products)


if __name__ == '__main__':
    while True:
        try:
            crawl()
        except Exception as e:
            print(e)

        time.sleep(3)
