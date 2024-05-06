# Generated by Django 5.0.4 on 2024-05-06 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='заголовок')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('body', models.TextField(verbose_name='содержимое')),
                ('img_preview', models.ImageField(blank=True, null=True, upload_to='catalog/posts/', verbose_name='превью (изображение)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='признак публикации')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
                'ordering': ('is_published',),
            },
        ),
    ]
