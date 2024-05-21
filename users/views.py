from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User, EmailVerification
from utils import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'


class UserRegisterView(TitleMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    title = 'Профиль'

    def get_object(self, queryset=None):
        """
        Метод для получения объекта пользователя.
        Переопределяется, чтобы не передавать pk текущего пользователя.
        """
        return self.request.user


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на подтверждение электронной почты.
        """
        key = kwargs['key']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, key=key)
        if email_verifications.exists():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('catalog:home'))
