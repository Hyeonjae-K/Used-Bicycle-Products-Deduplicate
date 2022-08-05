from django.shortcuts import render
from django.core.paginator import Paginator

from products.models import Product


def index(request):
    page = request.GET.get('page', '1')
    products = Product.objects.order_by('-create_date')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(page)
    return render(request, 'index.html', {'products': page_obj})
