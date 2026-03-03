import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from reservations.models import Reservation


class ReservationForm(forms.Form):
    """Форма для выбора свободного столика по заданным критериям"""

    start_time = forms.DateTimeField(
        label="Время начала бронирования",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )
    end_time = forms.DateTimeField(
        label="Время окончания бронирования",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )
    guests = forms.IntegerField(
        label="Количество гостей",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Укажите количество гостей"}
        ),
    )

    def clean_start_time(self):
        """Валидация даты и времени начала бронирования (не может быть в прошлом)"""
        start_time = self.cleaned_data.get("start_time")
        time_now = timezone.now()

        if not start_time:
            raise ValidationError("Укажите дату и время начала бронирования")

        if start_time:
            if start_time < time_now:
                raise ValidationError(
                    "Дата и время начала бронирования не может быть в прошлом"
                )

            if (
                datetime.time(hour=0, minute=0, second=0)
                < start_time.time()
                < datetime.time(hour=12, minute=0, second=0)
            ):
                raise ValidationError("Ресторан работает с 12-00 до 00-00")
        return start_time

    def clean_end_time(self):
        """Валидация даты и времени окончания бронирования (не может быть в прошлом)"""
        end_time = self.cleaned_data.get("end_time")
        time_now = timezone.now()

        if not end_time:
            raise ValidationError("Укажите дату и время окончания бронирования")

        if end_time:
            if end_time < time_now:
                raise ValidationError(
                    "Дата и время окончания бронирования не может быть в прошлом"
                )
            if (
                datetime.time(hour=0, minute=0, second=0)
                < end_time.time()
                < datetime.time(hour=12, minute=0, second=0)
            ):
                raise ValidationError("Ресторан работает с 12-00 до 00-00")
        return end_time

    def clean_guests(self):
        """Валидация количества гостей"""
        guests = self.cleaned_data.get("guests")
        if guests > 6:
            raise ValidationError("Максимальное количество гостей за столом - 6")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time:
            if start_time >= end_time:
                self.add_error(
                    "start_time",
                    "Время начала бронирования не может быть позже окончания бронирования",
                )
            elif end_time - start_time > datetime.timedelta(
                hours=12
            ) or end_time - start_time < datetime.timedelta(minutes=30):
                self.add_error(
                    "end_time",
                    "Бронирование не может длиться больше 12 часов или менее 30 минут",
                )
        return cleaned_data


class ReservationUpdateForm(forms.ModelForm):
    """Форма для редактирования бронирования с проверкой на занятость стола"""

    class Meta:
        model = Reservation
        exclude = ("user", "status", "created_at", "updated_at", "token")
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите количество гостей",
                }
            ),
        }

    def clean_start_time(self):
        """Валидация даты и времени начала бронирования (не может быть в прошлом)"""
        start_time = self.cleaned_data.get("start_time")
        time_now = timezone.now()

        if not start_time:
            raise ValidationError("Укажите дату и время начала бронирования")

        if start_time:
            if start_time < time_now:
                raise ValidationError(
                    "Дата и время начала бронирования не может быть в прошлом"
                )
        if (
            datetime.time(hour=0, minute=0, second=0)
            < start_time.time()
            < datetime.time(hour=12, minute=0, second=0)
        ):
            raise ValidationError("Ресторан работает с 12-00 до 00-00")
        return start_time

    def clean_end_time(self):
        """Валидация даты и времени окончания бронирования (не может быть в прошлом)"""
        end_time = self.cleaned_data.get("end_time")
        time_now = timezone.now()

        if not end_time:
            raise ValidationError("Укажите дату и время окончания бронирования")

        if end_time:
            if end_time < time_now:
                raise ValidationError(
                    "Дата и время окончания бронирования не может быть в прошлом"
                )
        if (
            datetime.time(hour=0, minute=0, second=0)
            < end_time.time()
            < datetime.time(hour=12, minute=0, second=0)
        ):
            raise ValidationError("Ресторан работает с 12-00 до 00-00")
        return end_time

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        table = cleaned_data.get("table")
        guests = cleaned_data.get("guests")

        if start_time and end_time:
            if start_time >= end_time:
                self.add_error(
                    "start_time",
                    "Время начала бронирования не может быть позже окончания бронирования",
                )
                return cleaned_data
            elif end_time - start_time > datetime.timedelta(
                hours=12
            ) or end_time - start_time < datetime.timedelta(minutes=30):
                self.add_error(
                    "end_time",
                    "Бронирование не может длиться больше 12 часов или менее 30 минут",
                )
                return cleaned_data

        if table and guests:
            if guests > table.seats:
                self.add_error(
                    "guests",
                    f"Выбранный стол не вмещает {guests} чел. Выберите другой стол или укажите иное количество гостей",
                )
                return cleaned_data

        conflict = (
            Reservation.objects.filter(
                table=table,
                status__in=[Reservation.CREATED, Reservation.CONFIRMED],
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            .exclude(pk=self.instance.pk)
            .exists()
        )

        if conflict:
            raise ValidationError(
                "На выбранное время этот столик уже занят. Выберите другое время."
            )

        return cleaned_data
