from django.conf.urls.static import static
from django.urls import path

from config import settings
from reservations.apps import ReservationsConfig
from reservations.views import (AboutView, HomeView, ReservationCheckView,
                                ReservationCreateView, ReservationDeleteView,
                                ReservationDetailView, ReservationListView,
                                ReservationUpdateView, TableListView,
                                reservation_verification)

app_name = ReservationsConfig.name


urlpatterns = [
    path("table/", TableListView.as_view(), name="table_list"),
    path("reservations/", ReservationListView.as_view(), name="reservation_list"),
    path(
        "reservations/check/",
        ReservationCheckView.as_view(),
        name="reservations_check",
    ),
    path(
        "reservations/create/",
        ReservationCreateView.as_view(),
        name="reservation_create",
    ),
    path(
        "reservations/confirm/<str:token>/",
        reservation_verification,
        name="reservation_confirm",
    ),
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
        name="reservation_delete",
    ),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
