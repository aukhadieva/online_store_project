from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='наименование категории')
    cat_desc = models.TextField(max_length=500, verbose_name='описание категории')
    manufactured_at = models.CharField(max_length=10, verbose_name='дата производства', **NULLABLE)

    def __str__(self):
        return f'{self.category_name} {self.cat_desc}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    prod_desc = models.TextField(max_length=500, verbose_name='описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    price = models.IntegerField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return (f'{self.product_name} {self.price} {self.prod_desc} {self.price} '
                f'{self.created_at} {self.updated_at}')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('in_stock',)
