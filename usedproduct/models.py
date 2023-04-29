from django.db import models

STORE_CHOICES = (
    ('중나', '중고나라'),
    ('번장', '번개장터'),
)


class Category(models.Model):
    store = models.CharField(max_length=2,  choices=STORE_CHOICES)
    name = models.CharField(max_length=25)
    url = models.URLField()


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    image = models.URLField()
    author = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
