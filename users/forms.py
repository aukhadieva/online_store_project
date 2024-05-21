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
