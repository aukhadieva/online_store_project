import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.timezone import now
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from users.models import User, EmailVerification
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

    def save(self, commit=True):
        user = super().save(commit=True)
        expiration = now() + timedelta(hours=48)
        verification = EmailVerification.objects.create(key=uuid.uuid4(), user=user, expiration=expiration)
        verification.send_verification_email()
        return user


class UserProfileForm(StyleMixin, UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """
    phone = PhoneNumberField(region="RU", widget=PhoneNumberPrefixWidget(country_choices=[("RU", "+7"),],),)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
