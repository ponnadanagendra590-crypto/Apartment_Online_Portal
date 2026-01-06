from django.urls import path
from .views import apartment_list

urlpatterns = [
    path('apartments/', apartment_list),
]
