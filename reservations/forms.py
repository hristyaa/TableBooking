from django import forms
from django.forms import ModelForm

from reservations.models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ("user", "status", "created_at", "updated_at", "token")
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
