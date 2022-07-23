from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from products.models import Product


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)


def crawl_jgnara():
    URL = 'https://m.cafe.naver.com/ca-fe/web/cafes/10050146/menus/432'
    row_selector = '#ct > div > div:nth-child(4) > ul > li > div'
    title_selector = 'a.txt_area > strong'
    author_selector = 'a.txt_area > div > span.nick > span'
    src_selector = 'a.thumb_area > div > picture > source'
    url_selector = 'div > a'
    driver.get(URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, row_selector)))

    rows = BeautifulSoup(driver.page_source,
                         'html.parser').select(row_selector)
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
