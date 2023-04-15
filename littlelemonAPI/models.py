from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = models.Index(fields=['price']),

# class MenuItem(models.Model):
#     title = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     inventory = models.SmallIntegerField()

class Category(models.Model):
    slug = models.SlugField()
    title= models.CharField (max_length=255)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title= models. CharField(max_length=255)
    price =models.DecimalField(max_digits=6, decimal_places=2)
    inventory =models.SmallIntegerField()
    category=models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title


class FoodItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()


    def __str__(self):
        return self.title

class Rating(models.Model):
    menuitem_id = models.SmallIntegerField()
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)