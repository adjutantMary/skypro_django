from django.db import models
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):

    objects = models.Manager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-category_name"]

    category_name = models.CharField("Наименование категории", max_length=128)
    category_description = models.TextField("Описание категории", max_length=255)

    def __str__(self):
        return self.category_name


class Product(models.Model):

    objects = models.Manager()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-product_name"]

    product_name = models.CharField("Наименование продукта", max_length=128)
    product_description = models.TextField("Описание продукта", max_length=255)
    product_preview = models.ImageField(
        "Изображение продукта", upload_to="catalog/photo", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category",
        verbose_name="Название категории",
    )
    product_cost = models.IntegerField("Цена за покупку")
    created_at = models.DateTimeField("Дата создания",  null=True)
    upload_at = models.DateTimeField("Дата последнего изменения", null=True)

    def __str__(self):
        return self.product_name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    objects = models.Manager()

    class Status(models.TextChoices):
        '''Класс для установки статуса поста'''

        # Draft - черновик, Published - опубликован
        # текущие перечисляемые типы, которые доступны
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField('Заголовок', max_length=128)
    slug = models.SlugField(max_length=250,
                            unique_for_date="publish")
    content = models.TextField('Содержимое')
    preview = models.ImageField('Превью', upload_to='posts/%Y/%m/%d/')
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    published = PublishedManager()
    views = models.IntegerField('Количество просмотров', default=0)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


    class Meta:
        ordering = ['-publish']

        # определение индекса базы данных по полю publish
        # индекс повышает производительность запросов, которые фильтруют или упорядочивают запросы по полю publish
        indexes = [
            models.Index(fields=['-publish'])
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    @staticmethod
    def get_absolute_url():
        return reverse('version_list')

