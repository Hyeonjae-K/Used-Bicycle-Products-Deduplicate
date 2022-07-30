from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    src = models.URLField(null=True, blank=True)
    url = models.URLField()
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}({self.author})'
