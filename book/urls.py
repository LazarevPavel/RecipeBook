from django.urls import path
from .views.test_view import TestView
from .views.recipe import RecipeView
from .views.product import ProductListView
from .views.recipe import RecipesListView

app_name = "book"


urlpatterns = [
    path('test', TestView.as_view()),
    path('recipe', RecipeView.as_view()),
    path('find_products', ProductListView.as_view()),
    path('find_recipes', RecipesListView.as_view())
]