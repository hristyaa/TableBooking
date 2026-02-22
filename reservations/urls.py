from django.urls import path
from reservations.apps import ReservationsConfig
from reservations.views import (
    home,
    TableListView,
    ReservationListView,
    ReservationCreateView,
    ReservationDetailView,
    ReservationUpdateView,
    ReservationDeleteView, reservation_verification,
)

app_name = ReservationsConfig.name


urlpatterns = [
    path("table/", TableListView.as_view(), name="table_list"),
    path("reservations/", ReservationListView.as_view(), name="reservation_list"),
    path(
        "reservations/create/",
        ReservationCreateView.as_view(),
        name="reservations_create",
    ),
    path("reservations/confirm/<str:token>/", reservation_verification, name='reservation_confirm'),
    path(
        "reservations/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservations_detail",
    ),
    path(
        "reservations/update/<int:pk>/",
        ReservationUpdateView.as_view(),
        name="reservation_update",
    ),
    path(
        "reservations/delete/<int:pk>/",
        ReservationDeleteView.as_view(),
        name="reservation_update",
    ),
    path("", home, name="home"),
]
