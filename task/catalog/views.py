from django.shortcuts import render, get_object_or_404

from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {"products": products,
               "categories": categories}
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_detail.html", context)


def contacts(request):
    return render(request, "contacts.html")

