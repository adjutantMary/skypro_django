from django.urls import path
from .views import home, contacts, product_detail


app_name = 'main'

urlpatterns = [
    path("", home, name='home'),
    path("contacts/", contacts),
    path("product/<int:pk>/", product_detail, name="product_detail"),
]
