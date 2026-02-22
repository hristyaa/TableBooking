from django.forms import ModelForm
from django import forms
from reservations.models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ('user', 'status', 'created_at', 'updated_at', 'token')
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

