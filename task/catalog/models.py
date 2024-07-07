from django.db import models


class Category(models.Model):

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-category_name']

    category_name = models.CharField('Наименование категории', max_length=128)
    category_description = models.TextField('Описание категории', max_length=255)

    def __str__(self):
        return self.category_name


class Product(models.Model):

    objects = models.Manager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-product_name']

    product_name = models.CharField('Наименование продукта', max_length=128)
    product_description = models.TextField('Описание продукта', max_length=255)
    product_preview = models.ImageField('Изображение продукта',
                                        upload_to='catalog/photo',
                                        blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='category',
        verbose_name='Название категории'
    )
    product_cost = models.IntegerField('Цена за покупку')
    created_at = models.DateTimeField('Дата создания')
    upload_at = models.DateTimeField('Дата последнего изменения')

    def __str__(self):
        return self.product_name
