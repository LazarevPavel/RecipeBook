from django.db import models
from .product import Product
from users.models.user import CustomUser


class Recipe(models.Model):
    """Рецепт"""
    classname = 'recipe'

    name = models.CharField(max_length=255, null=False)
    instructions = models.TextField(max_length=16383)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='recipe')
    products_for = models.ManyToManyField(Product, through='Ingredients', through_fields=('recipe', 'product'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} --- {}'.format(self.id, self.name)

