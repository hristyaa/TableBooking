from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    "Форма для регистрации пользователя."

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
