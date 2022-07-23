from django.shortcuts import render

from apscheduler.schedulers.background import BackgroundScheduler

from products.models import Product
from crawlers import products

sched = BackgroundScheduler()
sched.add_job(products.crawl_jgnara, 'interval', seconds=5)
sched.start()


def index(request):
    products = Product.objects.order_by('-create_date')
    return render(request, 'index.html', {'products': products})
