from django.contrib import admin
from .models import *


class MyAdminSite(admin.AdminSite):
    site_header = "Информация о продуктах"


shop_admin = MyAdminSite(name="shop-admin")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "category", "product_cost")
    list_filter = ("category",)
    search_fields = ("product_name", "product_description")
    search_help_text = "Поиск работает по названию продукта или его описанию"
    actions = ['publish_products', 'unpublish_products']

    @admin.action(description="Опубликовать выбранные продукты")
    def publish_products(self, request, queryset):
        queryset.update(is_published=True)
        
    @admin.action(description="Опубликовать выбранные продукты")
    def unpublish_products(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

shop_admin.register(Product, ProductAdmin)
shop_admin.register(Category, CategoryAdmin)
shop_admin.register(Post, PostAdmin)
