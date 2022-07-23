from django.shortcuts import render

from products.models import Product


def index(request):
    print('index')
    products = Product.objects.order_by('-create_date')
    return render(request, 'index.html', {'products': products})
