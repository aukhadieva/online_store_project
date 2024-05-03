from django.db import models
from pytils.templatetags.pytils_translit import slugify

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='наименование категории')
    cat_desc = models.TextField(max_length=500, verbose_name='описание категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    prod_desc = models.TextField(verbose_name='описание продукта')
    image = models.ImageField(upload_to='catalog/products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата изменения')
    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('in_stock',)


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя')
    email = models.EmailField(max_length=254, verbose_name='электронная почта')
    message = models.TextField(max_length=1000, verbose_name='сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'


class BlogPost(models.Model):
    title = models.CharField(max_length=50, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    # slug = models.SlugField(unique=True)
    body = models.TextField(verbose_name='содержимое')
    img_preview = models.ImageField(upload_to='catalog/posts/', verbose_name='превью (изображение)', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('is_published',)
