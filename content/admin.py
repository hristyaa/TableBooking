from django.contrib import admin

from content.models import (AboutPage, Contacts, Feedback, HomePage, Services,
                            Staff, Values)

# Register your models here.


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "hall_title", "terrace_title", "is_active")
    search_fields = ("title",)
    ordering = ("id",)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant_name", "phone", "email", "address", "work_hours")
    search_fields = ("restaurant_name",)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "message", "created_at")
    search_fields = ("name",)
    ordering = ("created_at",)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "history",
        "mission",
    )


@admin.register(Values)
class ValuesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "description", "photo")
    search_fields = ("name",)
    ordering = ("id",)
