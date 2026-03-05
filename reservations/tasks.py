from celery import shared_task
from django.utils import timezone

from reservations.models import Reservation


@shared_task
def mark_completed_reservations():
    """Перевод в статус 'Завершено' бронирование, окончание бронирование которого прошло"""
    return Reservation.objects.filter(
        status__in=[Reservation.CREATED, Reservation.CONFIRMED],
        end_time__lt=timezone.now(),
    ).update(status=Reservation.COMPLETED)
