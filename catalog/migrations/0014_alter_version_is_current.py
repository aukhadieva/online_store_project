# Generated by Django 5.0.4 on 2024-05-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_version_is_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='признак текущей версии'),
        ),
    ]
