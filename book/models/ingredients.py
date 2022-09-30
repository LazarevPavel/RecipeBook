from django.db import models
from .product import Product
from .recipe import Recipe


class Ingredients(models.Model):
    """Ингредиенты для рецепта"""
    classname = 'ingredients'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    howmany = models.FloatField(null=False)
    measure = models.CharField(max_length=30, null=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return "{} --- {}".format(self.product.name, self.recipe.name)
