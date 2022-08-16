from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    src = models.URLField(null=True, blank=True, max_length=1024)
    url = models.URLField(max_length=1024)
    market = models.CharField(max_length=8, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}({self.author})'
