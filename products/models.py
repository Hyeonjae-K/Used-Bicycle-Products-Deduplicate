from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    src = models.URLField(null=True, blank=True)
    url = models.URLField()
    update_date = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}({self.author})'
