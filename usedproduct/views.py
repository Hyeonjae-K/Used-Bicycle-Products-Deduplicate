from django.shortcuts import render
from django.core.paginator import Paginator

from usedproduct.models import Product, Category

COUNT_PER_PAGE = 30


def index(request):
    page = request.GET.get('page', '1')
    paginator = Paginator(
        Product.objects.order_by('-created_at'),
        COUNT_PER_PAGE
    )
    products = paginator.get_page(page)

    return render(request, 'views/index.html', {'products': products})
