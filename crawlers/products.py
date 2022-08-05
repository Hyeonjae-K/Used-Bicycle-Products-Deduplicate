from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from products.models import Product


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)


def parse_jg(rows):
    title_selector = 'a.txt_area > strong'
    author_selector = 'a.txt_area > div > span.nick > span'
    src_selector = 'a.thumb_area > div > picture > source'
    url_selector = 'div > a'

    new_objects = []
    update_objects = []
    for row in rows:
        if not row.text:
            continue

        title = row.select_one(title_selector).text
        author = row.select_one(author_selector).text
        url = row.select_one(url_selector).get('href')
        src = row.select_one(src_selector).get(
            'srcset') if row.select_one(src_selector) else None

        if product := Product.objects.filter(title=title, author=author).first():
            product.src = src
            product.url = url
            update_objects.append(product)
        else:
            new_objects.append(
                Product(title=title, author=author, src=src, url=url))

    if new_objects:
        Product.objects.bulk_create(new_objects)
    if update_objects:
        Product.objects.bulk_update(update_objects, fields=['src', 'url'])


def parse_bj(cards):
    title_selector = 'div:nth-child(2) > div:nth-child(1)'
    url_prefix = 'https://m.bunjang.co.kr'
    src_selector = 'a > div > img'
    price_selector = 'a > div:nth-child(2) > div:nth-child(2) > div'
    location_selector = 'a > div:nth-child(3)'

    titles = [card.select_one(title_selector).text for card in cards]
    urls = [url_prefix + card.get('href')[:card.get('href').find('?')]
            for card in cards]
    srcs = [card.select_one(src_selector).get('src') for card in cards]
    prices = [None if (price := card.select_one(price_selector).text)
              == '연락요망' else int(''.join(price.split(','))) for card in cards]
    locations = [card.select_one(location_selector).text for card in cards]

    products = [Product(title=title, url=url, src=src, price=price, location=location) for title, url, src,
                price, location in zip(titles, urls, srcs, prices, locations) if not Product.objects.filter(url=url)]
    Product.objects.bulk_create(products)


def crawl():
    global driver

    # jg
    jg_url = 'https://m.cafe.naver.com/ca-fe/web/cafes/10050146/menus/432'
    jg_row_selector = '#ct > div > div:nth-child(4) > ul > li > div'
    try:
        driver.get(jg_url)
    except WebDriverException:
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', chrome_options=options)
        driver.get(jg_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, jg_row_selector)))

    jg_rows = BeautifulSoup(
        driver.page_source, 'html.parser').select(jg_row_selector)
    parse_jg(jg_rows)

    # bj
    bj_url = 'https://m.bunjang.co.kr/categories/700350500?&order=date'
    bj_card_selector = '#root > div > div > div:nth-child(4) > div > div:nth-child(3) > div > div > a'
    try:
        driver.get(bj_url)
    except WebDriverException:
        driver = webdriver.Chrome(
            '/usr/bin/chromedriver', chrome_options=options)
        driver.get(bj_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, bj_card_selector)))

    cards = BeautifulSoup(driver.page_source,
                          'html.parser').select(bj_card_selector)
    parse_bj(cards)
