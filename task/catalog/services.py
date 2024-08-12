from django.core.cache import cache

from .models import Category


def get_categories():
    categories = cache.get('categories')
    if categories:
        print('Категории в кэше')
    else:
        print('Категории не найдены в кэше')
        
    if not categories:
        categories = list(Category.objects.all())
        cache.set('categories', categories, timeout=5)
    return categories