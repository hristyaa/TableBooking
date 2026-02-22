import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config import settings
from reservations.forms import ReservationForm
from reservations.models import Reservation, Table

# Create your views here.


def home(request):
    return render(request, "reservations/home.html")


class TableListView(ListView):
    model = Table
    context_object_name = "tables"

    def get_context_data(self, **kwargs):
        # Вызов метода get_context_data() базового класса с помощью super
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context["tables_hall"] = Table.objects.filter(
            location=Table.HALL, is_active=True
        ).order_by("id")
        context["tables_terrace"] = Table.objects.filter(
            location=Table.TERRACE, is_active=True
        ).order_by("id")
        return context


class ReservationListView(ListView):
    model = Reservation
    context_object_name = "reservations"


class ReservationDetailView(DetailView):
    model = Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:reservation_list")

    def form_valid(self, form):
        """
        Посетитель = создатель бронирования(авторизованный пользователь)
        Подтверждение бронирования через email
        """
        reservation = form.save(commit=False)
        user = self.request.user
        reservation.user = user
        token = secrets.token_hex(16)
        reservation.token = token
        reservation.save()
        host = self.request.get_host()
        url = f"http://{host}/reservations/confirm/{token}/"
        send_mail(
            subject="Подтверждение бронирования",
            message=f"Здравствуйте, перейдите по ссылки для подтверждения бронирования {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def reservation_verification(request, token):
    """Подтверждение бронирования при переходе по ссылке на email"""
    reservation = get_object_or_404(Reservation, token=token)
    reservation.status = Reservation.CONFIRMED
    reservation.save()
    return redirect("reservations:reservation_list")


class ReservationUpdateView(UpdateView):
    model = Reservation


class ReservationDeleteView(DeleteView):
    model = Reservation
