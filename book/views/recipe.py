from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist

from ..models.recipe import Recipe
from ..models.ingredients import Ingredients
from ..models.product import Product
from unwolfable.base.base_renderer import BaseJSONRenderer
from ..serializers.recipe import RecipeSerializer, RecipesListSerializer


class RecipesPagination(LimitOffsetPagination):
    '''Распил списка рецептов на куски по default_limit штук или по указанному пользователем лимиту'''
    default_limit = 5
    max_limit = 100


class RecipeView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = RecipeSerializer

    def get(self, request):
        recipe_id = request.data.get('id', None)
        if recipe_id:
            recipe = Recipe.objects.get(id=recipe_id)
            serializer = self.serializer_class(instance=recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        recipe = request.data.get('data', {})

        serializer = self.serializer_class(data=recipe)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            if data.get('ingredients'):
                recipe = Recipe(name=data['name'],
                                instructions=data['instructions'],
                                author=request.user)
                recipe.save()

                # будем фильтровать сначала по имени, в противом случае по id
                # что-то одно из этого точно будет
                for ingredient in data['ingredients']:
                    product_query = Q(name=ingredient.get('product').get('name')) \
                        if ingredient.get('product').get('name') \
                        else Q(id=ingredient.get('product').get('id'))

                    Ingredients(product=Product.objects.get(product_query),
                                recipe=recipe,
                                howmany=ingredient.get('howmany'),
                                measure=ingredient.get('measure')).save()

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request):
        data = request.data.get('data', {})

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                recipe = Recipe.objects.get(id=data.get('id'))
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if recipe.author.id != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            is_differs = False
            if recipe.name != data.get('name'):
                recipe.name = data.get('name')
                is_differs = True
            if recipe.instructions != data.get('instructions'):
                recipe.instructions = data.get('instructions')
                is_differs = True

            ingredients_new = data.get('products_for')
            ingredients_old = list(Ingredients.objects.filter(recipe=recipe))
            create_update_list = []
            for new_ingr in ingredients_new:
                old_has_ingr = False

                for old_ingr in ingredients_old:
                    if new_ingr['product']['id'] == old_ingr.product.id:
                        old_has_ingr = True

                        is_edited = False
                        if new_ingr['howmany'] != old_ingr.howmany:
                            old_ingr.howmany = new_ingr['howmany']
                            is_edited = True
                        if new_ingr['measure'] != old_ingr.measure:
                            old_ingr.measure = new_ingr['measure']
                            is_edited = True

                        if is_edited:
                            create_update_list.append(old_ingr)

                        ingredients_old.pop(
                            ingredients_old.index(old_ingr)
                        )
                        break

                if not old_has_ingr:
                    create_update_list.append(
                        Ingredients(product=Product.objects.get(id=new_ingr['product']['id']),
                                    recipe=recipe,
                                    howmany=new_ingr['howmany'],
                                    measure=new_ingr['measure'])
                    )

                ingredients_new.pop(
                    ingredients_new.index(new_ingr)
                )

            for old_ingr in ingredients_old:
                old_ingr.delete()
            for ingr in create_update_list:
                ingr.save()
            if is_differs:
                recipe.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        recipe = request.data.get('id', None)
        if recipe:
            recipe = Recipe.objects.get(id=recipe)
            if recipe.author.username == request.user.username:
                ingredients = Ingredients.objects.filter(recipe=recipe)
                ingredients.delete()
                recipe.delete()
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------

class RecipesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = RecipesListSerializer
    pagination_class = RecipesPagination

    def get_queryset(self):
        #фильтр рецептов по автору, названию, необходимым ингредиентам

        params = self.request.data
        query = Q()

        if params.get('author'):
            query = query & Q(author__username__startswith=params.get('author'))
        if params.get('name'):
            query = query & Q(name__icontains=params.get('name'))
        if params.get('ingredients'):
            #получим рецепты, соответствующие по автору и названию, или возьмём все
            recipes_qs = Recipe.objects.filter(query)

            #дальше среди них отбираем те рецепты, в которых есть заданные ингредиенты
            ingredients = params.get('ingredients')
            recipes_with_ingredients_qs = Ingredients.objects.filter(recipe__id__in=recipes_qs,
                                                                     product__id__in=ingredients) \
                                                             .values('recipe') \
                                                             .distinct('recipe')

            # запрашиваем рецепты с сортировкой их по трём параметрам:
            # ingr_matches_count - количество совпадающих ингредиентов рецепта с ингредиентами в запросе пользователя
            # ingr_fully_count - полное количество ингредиентов в рецепте
            # created_at - дата публикации
            result_recipes_qs = Recipe.objects.annotate(ingr_matches_count=Count('ingredients',
                                                                                 filter=Q(ingredients__product__id__in=ingredients))
                                                        )\
                .annotate(ingr_fully_count=Count('products_for')) \
                .filter(id__in=recipes_with_ingredients_qs) \
                .order_by('-ingr_matches_count', 'ingr_fully_count', '-created_at')

            return result_recipes_qs

        return Recipe.objects.filter(query).order_by('-created_at')
