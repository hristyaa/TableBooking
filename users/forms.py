from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from users.models import User


class UserRegisterForm(UserCreationForm):
    "Форма для регистрации пользователя."

    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя"}
        ),
    )

    email = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите email"}
        ),
    )

    phone = PhoneNumberField(
        required=False,
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер телефона"}
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повторите пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "email", "phone", "password1", "password2")


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
