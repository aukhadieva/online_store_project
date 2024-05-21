from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
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
