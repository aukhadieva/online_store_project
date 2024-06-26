from django.db import models
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=50, verbose_name='заголовок')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=False)
    body = models.TextField(verbose_name='содержимое')
    img_preview = models.ImageField(upload_to='blog/posts/', verbose_name='превью (изображение)', **NULLABLE)
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
