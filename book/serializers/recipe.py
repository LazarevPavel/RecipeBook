from rest_framework import serializers

from ..models.recipe import Recipe
from .ingredients import IngredientsSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    products_for = IngredientsSerializer(source='ingredients', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'author', 'products_for']


class RecipesListSerializer(serializers.ModelSerializer):
    """Сериализатор списка рецептов"""
    INSTRUCTIONS_CHARS_LIMIT = 255

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'author']
        read_only_fields = ['id', 'author']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if len(ret['instructions']) > self.INSTRUCTIONS_CHARS_LIMIT:
            ret['instructions'] = ret['instructions'][:self.INSTRUCTIONS_CHARS_LIMIT]

        return ret
