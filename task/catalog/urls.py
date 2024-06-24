
from django.urls import path
from .views import home, contacts

urlpatterns = [
    path('', home),
    path('contacts/', contacts)
]