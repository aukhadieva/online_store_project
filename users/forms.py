from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User
from utils import StyleMixin


class UserLoginForm(StyleMixin, AuthenticationForm):
    """
    Форма для авторизации и аутентификации пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserRegisterForm(StyleMixin, UserCreationForm):
    """
    Форма для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleMixin, UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
