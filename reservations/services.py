from reservations.models import Reservation, Table


class ReservationService:

    @staticmethod
    def selection_tables(guests, start_time, end_time):
        """Сервис для подбора свободных столиков."""
        busy_tables = Reservation.objects.filter(
            status__in=[Reservation.CREATED, Reservation.CONFIRMED],
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        available_tables = Table.objects.filter(
            is_active=True, seats__gte=guests
        ).exclude(reservations__in=busy_tables)

        return available_tables.order_by("seats", "id")
