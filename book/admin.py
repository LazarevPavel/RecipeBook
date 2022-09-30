from django.contrib import admin

from .models import Ingredients, Product, Recipe

# Register your models here.
admin.site.register(Ingredients)
admin.site.register(Product)
admin.site.register(Recipe)

