from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='наименование категории')
    cat_desc = models.TextField(max_length=500, verbose_name='описание категории')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    prod_desc = models.TextField(max_length=500, verbose_name='описание продукта')
    image = models.ImageField(upload_to='catalog/products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата изменения')
    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return f'{self.product_name} {self.category} {self.price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('in_stock',)


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя')
    email = models.EmailField(max_length=254, verbose_name='электронная почта')
    message = models.TextField(max_length=1000, verbose_name='сообщение')

    def __str__(self):
        return f'{self.name} {self.email} {self.message}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
