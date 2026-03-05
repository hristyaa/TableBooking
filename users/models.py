from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Укажите адрес электронной почты",
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", help_text="Укажите имя"
    )
    phone = PhoneNumberField(
        blank=True, verbose_name="Номер телефона", help_text="Укажите номер телефона"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
