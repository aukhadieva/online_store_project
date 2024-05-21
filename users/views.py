from django.contrib.auth.views import LoginView
from django.shortcuts import render

from users.forms import UserLoginForm
from users.models import User


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
