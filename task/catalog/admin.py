from django.contrib import admin
from .models import Product, Category


class MyAdminSite(admin.AdminSite):
    site_header = "Информация о продуктах"


shop_admin = MyAdminSite(name="shop-admin")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "category", "product_cost")
    list_filter = ("category",)
    search_fields = ("product_name", "product_description")
    search_help_text = "Поиск работает по названию продукта или его описанию"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")


shop_admin.register(Product, ProductAdmin)
shop_admin.register(Category, CategoryAdmin)
