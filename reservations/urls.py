from django.urls import path
from reservations.apps import ReservationsConfig
from reservations.views import home

app_name = ReservationsConfig.name


urlpatterns = [
    path('', home, name='home'),
]
