from django.db import models

from users.models import User

# Create your models here.


class Table(models.Model):
    """Модель столика в ресторане."""

    HALL = "hall"
    TERRACE = "terrace"

    LOCATION = [
        (HALL, "В зале"),
        (TERRACE, "На терассе"),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Наименование (номер) столика",
        help_text="Укажите наименование столика",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Описание столика",
        help_text="Укажите описание столика",
    )
    location = models.CharField(
        max_length=20,
        choices=LOCATION,
        default=HALL,
        verbose_name="Местоположение столика",
        help_text="Выберите местоположение столика",
    )
    seats = models.PositiveIntegerField(
        verbose_name="Вместимость столика", help_text="Укажите вместимость столика"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Подлежит бронированию",
        help_text="Отметьте, подлежит ли столик бронированию",
    )

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} ({self.get_location_display()}) -  {str(self.seats)} чел."


class Reservation(models.Model):
    """Модель бронирования."""

    CREATED = "created"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

    RESERVATION_STATUS = [
        (CREATED, "Создано"),
        (CONFIRMED, "Подтверждено"),
        (CANCELED, "Отменено"),
        (COMPLETED, "Завершено"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Посетитель",
        help_text="Укажите посетителя",
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name="Столик",
        help_text="Выберите столик",
        related_name="reservations",
    )
    start_time = models.DateTimeField(
        verbose_name="Время начала бронирования",
        help_text="Укажите, на какое время хотите забронированить столик",
    )
    end_time = models.DateTimeField(
        verbose_name="Время окончания бронирования",
        help_text="Укажите, в какое время готовы освободить столик",
    )
    guests = models.PositiveIntegerField(
        verbose_name="Количество гостей", help_text="Укажите количество гостей"
    )
    status = models.CharField(
        max_length=20,
        choices=RESERVATION_STATUS,
        default=CREATED,
        verbose_name="Статус бронирования",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания бронирования"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата изменения бронирования"
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.table} ({self.status}) в {self.start_time}"
