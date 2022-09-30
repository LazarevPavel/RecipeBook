from rest_framework import serializers

from ..models.ingredients import Ingredients
from ..models.recipe import Recipe

from .product import ProductSerializer


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    product = ProductSerializer()
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Ingredients
        fields = ['id', 'product', 'recipe', 'howmany', 'measure']
