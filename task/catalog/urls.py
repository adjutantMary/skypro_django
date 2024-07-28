from django.urls import path
from .views import *


app_name = "main"

urlpatterns = [
    path("", ProductTemplateView.as_view(), name="product_list"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("post_list/", PostListView.as_view(), name='post_list'),
    path("<slug:slug>/", PostDetailView.as_view(), name='post_detail'),
    path("post_list/create/", PostCreateView.as_view(), name='create_view'),
    path("<slug:slug>/update/", PostUpdateView.as_view(), name='post_update'),
    path("<slug:slug>/delete/", PostDeleteView.as_view(), name='post_delete'),
]
