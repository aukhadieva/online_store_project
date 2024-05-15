from django.db import models

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
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата изменения')
    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('in_stock',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="version", verbose_name='продукт')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    version_number = models.IntegerField(verbose_name='номер версии')
    is_current = models.BooleanField(default=True, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.version_name} / {self.version_number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('is_current',)


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя')
    email = models.EmailField(max_length=254, verbose_name='электронная почта')
    message = models.TextField(max_length=1000, verbose_name='сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
