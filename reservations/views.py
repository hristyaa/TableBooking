import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    FormView,
    View,
)

from config import settings
from reservations.forms import ReservationForm, ReservationUpdateForm
from reservations.models import Reservation, Table
from reservations.services import ReservationService

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
    ordering = [
        "status",
    ]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by(
            "-start_time"
        )


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    context_object_name = "reservation"


class ReservationCheckView(LoginRequiredMixin, FormView):
    form_class = ReservationForm
    template_name = "reservations/reservation_check.html"

    def form_valid(self, form):
        data = form.cleaned_data

        available_tables = ReservationService.selection_tables(
            guests=data.get("guests"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )

        return render(
            self.request,
            self.template_name,
            {"form": form, "tables": available_tables, "form_data": form.cleaned_data},
        )


# class ReservationCreateView(LoginRequiredMixin, CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     success_url = reverse_lazy("reservations:reservation_list")
#
#     def form_valid(self, form):
#         """
#         Посетитель = создатель бронирования(авторизованный пользователь)
#         Подтверждение бронирования через email
#         """
#         reservation = form.save(commit=False)
#         user = self.request.user
#         reservation.user = user
#         token = secrets.token_hex(16)
#         reservation.token = token
#         reservation.save()
#         host = self.request.get_host()
#         url = f"http://{host}/reservations/confirm/{token}/"
#         send_mail(
#             subject="Подтверждение бронирования",
#             message=f"Здравствуйте, перейдите по ссылки для подтверждения бронирования {url}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#         )
#         return super().form_valid(form)


class ReservationCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)

        if not form.is_valid():
            print(form.errors)
            return redirect("reservations:reservations_check")

        table = get_object_or_404(
            Table, id=request.POST.get("table_id"), is_active=True
        )
        token = secrets.token_hex(16)

        Reservation.objects.create(
            user=request.user,
            table=table,
            start_time=form.cleaned_data["start_time"],
            end_time=form.cleaned_data["end_time"],
            guests=form.cleaned_data["guests"],
            status=Reservation.CREATED,
            token=token,
        )

        host = self.request.get_host()
        url = f"http://{host}/reservations/confirm/{token}/"
        send_mail(
            subject="Подтверждение бронирования",
            message=f"Здравствуйте, перейдите по ссылкe для подтверждения бронирования {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )

        return redirect("reservations:reservation_list")


def reservation_verification(request, token):
    """Подтверждение бронирования при переходе по ссылке на email"""
    reservation = get_object_or_404(Reservation, token=token)
    reservation.status = Reservation.CONFIRMED
    reservation.token = None
    reservation.save()
    return redirect("reservations:reservation_list")


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm
    context_object_name = "reservation"
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservations:reservation_list")

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user,
            status__in=[Reservation.CONFIRMED, Reservation.CREATED],
        )

    def get_success_url(self):
        return reverse("reservations:reservations_detail", args=[self.kwargs.get("pk")])

    def form_valid(self, form):
        """
        Авторизованный пользователь = создатель бронирования
        Подтверждение бронирования через email
        """
        reservation = form.save(commit=False)
        reservation.status = Reservation.CREATED
        token = secrets.token_hex(16)
        reservation.token = token
        host = self.request.get_host()
        url = f"http://{host}/reservations/confirm/{token}/"
        send_mail(
            subject="Подтверждение изменения бронирования",
            message=f"Здравствуйте, перейдите по ссылкe для подтверждения бронирования {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[reservation.user.email],
        )
        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    context_object_name = "reservation"
    template_name = "reservations/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservations:reservation_list")

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = Reservation.CANCELED
        self.object.save(update_fields=["status"])
        return HttpResponseRedirect(self.success_url)
