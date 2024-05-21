from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from config import settings
from config.settings import DOMAIN_NAME

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

    def send_verification_email(self):
        """
        Отправляет электронное письмо с ключом подтверждения эл. почты.
        """
        link = reverse('users:verify', kwargs={'email': self.user.email, 'key': self.key})
        verification_link = f'{DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи'
        message = f'Для подтверждения регистрации пройдите по ссылке:\n {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        """
        Проверяет, истек ли срок действия ключа.
        """
        return True if now() >= self.expiration else False
