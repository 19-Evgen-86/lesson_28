from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)


class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    price = models.IntegerField
    description = models.TextField
    address = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
