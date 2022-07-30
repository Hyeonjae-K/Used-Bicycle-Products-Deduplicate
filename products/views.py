from django.shortcuts import render
from django.core.paginator import Paginator

from apscheduler.schedulers.background import BackgroundScheduler

from products.models import Product
from crawlers import products

sched = BackgroundScheduler()
sched.add_job(products.crawl_jg, 'interval', seconds=1)
sched.add_job(products.crawl_bj, 'interval', seconds=1)
sched.start()


def index(request):
    page = request.GET.get('page', '1')
    products = Product.objects.order_by('-create_date')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(page)
    return render(request, 'index.html', {'products': page_obj})
