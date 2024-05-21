from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=70, verbose_name='страна', **NULLABLE)
    is_verified_email = models.BooleanField(default=False, verbose_name='статус подтверждения эл. почты')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class EmailVerification(models.Model):
    key = models.UUIDField(unique=True, verbose_name='ключ')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='пользователь')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата генерации ключа')
    expiration = models.DateTimeField(verbose_name='срок действия ключа')

    def __str__(self):
        return f'Email verification for {self.user}'

    class Meta:
        verbose_name = 'проверка электронной почты'
