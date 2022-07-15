from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=100, blank=True)
    description = models.TextField(default="", blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    categories = models.ManyToManyField(Categories)
    image = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
