from django.urls import path
from .views.registration import RegistrationView


app_name = "users"


urlpatterns = [
    path('register/', RegistrationView.as_view()),
]