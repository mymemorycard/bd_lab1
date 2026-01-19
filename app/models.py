from django.db import models


class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class ProductURL(models.Model):
    url = models.TextField()

    @property
    def shop_name(self):
        return self.url.split("/")[2]

    def __str__(self):
        return self.url


class Book(models.Model):
    isbn = models.TextField(unique=True, null=True)

    name = models.TextField(unique=True)
    author = models.TextField(null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    release_year = models.PositiveSmallIntegerField(null=True)

    genre = models.ManyToManyField(Genre)
    product_urls = models.ManyToManyField(ProductURL)

    def __str__(self):
        return self.name
