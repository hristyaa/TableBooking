from django.contrib import admin

from reservations.models import Reservation, Table

# Register your models here.


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "seats",
        "description",
        "is_active",
    )
    search_fields = (
        "name",
        "seats",
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "table", "start_time", "end_time", "status")
    search_fields = (
        "table",
        "status",
    )
