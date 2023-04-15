from django.contrib import admin
from .models import Book, Category, MenuItem, FoodItem, Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Rating)