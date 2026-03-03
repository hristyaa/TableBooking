from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.forms import FeedbackForm
from content.models import (AboutPage, Contacts, HomePage, Services, Staff,
                            Values)
from reservations.forms import ReservationForm
from reservations.models import Reservation, Table
from users.models import User

# Create your tests here.


class ReservationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.user.set_password("1234")
        self.user.save()

        self.user_2 = User.objects.create(email="test2@test.ru")
        self.user_2.set_password("1234")
        self.user_2.save()

        self.table = Table.objects.create(
            name="test table",
            seats=6,
        )
        self.table_2 = Table.objects.create(
            name="test table 2",
            seats=4,
        )
        start_time = datetime.strptime('2026.03.03 12:10:00', '%Y.%m.%d %H:%M:%S')
        end_time = start_time + timedelta(hours=1)

        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            start_time=start_time,
            end_time=end_time,
            guests=4,
            status=Reservation.CONFIRMED,
        )

        self.reservation_2 = Reservation.objects.create(
            user=self.user_2,
            table=self.table_2,
            start_time=start_time,
            end_time=end_time,
            guests=4,
            status=Reservation.CANCELED,
        )

    def test_reservation_form_validation(self):
        """Проверка валидации формы ReservationForm"""
        self.client.login(email=self.user.email, password="1234")
        start = datetime.strptime('2026.03.03 12:10:00', '%Y.%m.%d %H:%M:%S')
        end = start + timedelta(hours=2)
        data_invalid = {
            "table_id": self.table_2.id,
            "start_time": start,
            "end_time": end,
            "guests": 10,
        }

        form = ReservationForm(data=data_invalid)
        self.assertFalse(form.is_valid())
        self.assertIn("guests", form.errors)
        self.assertIn(
            "Максимальное количество гостей за столом - 6", form.errors["guests"]
        )
        data = {
            "table_id": self.table_2.id,
            "start_time": start,
            "end_time": end,
            "guests": 4,
        }
        form = ReservationForm(data=data)
        if not form.is_valid():
            print("Ошибки формы:", form.errors)
            print("Ошибки не полей:", form.non_field_errors())

        self.assertTrue(form.is_valid())

    def test_create_reservation(self):
        """Тест на создание бронирования"""
        self.client.login(email=self.user_2.email, password="1234")

        url = reverse("reservations:reservation_create")
        start = datetime.strptime('2026.03.03 14:10:00', '%Y.%m.%d %H:%M:%S')
        end = start + timedelta(hours=2)

        data = {
            "table_id": self.table_2.id,
            "start_time": start,
            "end_time": end,
            "guests": 2,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Reservation.objects.count(), 3)
        self.assertTrue(
            Reservation.objects.filter(
                user=self.user_2, table=self.table_2, guests=2
            ).exists()
        )

    def test_detail_reservation(self):
        """Тест на детальный просмотр бронирования"""
        self.client.login(email=self.user.email, password="1234")
        url = reverse("reservations:reservations_detail", args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.reservation.guests))

    def test_delete_reservation(self):
        """Тестирование удаления бронирования (отмены без фактического удаления, с измененим статуса)"""
        self.client.login(email=self.user.email, password="1234")
        url = reverse("reservations:reservation_delete", args=[self.reservation.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("reservations:reservation_list"))

        self.assertEqual(Reservation.objects.count(), 2)
        # обновление бд для проверки статуса бронирования
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "canceled")

    def test_update_reservation(self):
        """Тестирование изменения бронирования"""
        self.client.login(email=self.user.email, password="1234")
        url = reverse("reservations:reservation_update", args=[self.reservation.id])
        start = datetime.strptime('2026.03.03 12:10:00', '%Y.%m.%d %H:%M:%S')
        end = start + timedelta(hours=2)

        data = {
            "table": self.table_2.id,
            "start_time": start.strftime('%Y.%m.%d %H:%M:%S'),
            "end_time": end.strftime('%Y.%m.%d %H:%M:%S'),
            "guests": 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.table.id, self.table_2.id)
        self.assertEqual(self.reservation.guests, 2)

        # проверка, что user не сможет изменить объект, созданный user_2
        url = reverse("reservations:reservation_update", args=[self.reservation_2.id])
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, 404)
        data = {
            "table": self.table.id,
            "start_time": start.strftime('%Y.%m.%d %H:%M:%S'),
            "end_time": end.strftime('%Y.%m.%d %H:%M:%S'),
            "guests": 4,
        }
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 404)
        self.reservation_2.refresh_from_db()
        self.assertEqual(self.reservation_2.table.id, self.table_2.id)

    def test_reservation_list(self):
        self.client.login(email=self.user.email, password="1234")
        url = reverse("reservations:reservation_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/reservation_list.html")
        self.assertEqual(len(response.context["reservations"]), 1)


class SitePagesTest(TestCase):
    def setUp(self):
        self.home = HomePage.objects.create(
            title="Тестовый ресторан",
            subtitle="Тестовое описание",
            hall_title="Тестовый зал",
            is_active=True,
        )
        self.contacts = Contacts.objects.create(
            restaurant_name="Ресторан", address="Тест адрес"
        )
        self.service_1 = Services.objects.create(name="Сервис 1")
        self.service_2 = Services.objects.create(name="Сервис 2")

        self.values_1 = Values.objects.create(name="Ценность 1")
        self.values_2 = Values.objects.create(name="Ценность 2")

        self.about = AboutPage.objects.create(
            history="История тест",
            mission="Миссия тест",
        )
        self.about.values.add(self.values_1, self.values_2)

        self.staff_1 = Staff.objects.create(name="Сотрудник 1", role="Администратор")
        self.staff_2 = Staff.objects.create(name="Сотрудник 2", role="Повар")

    def test_home_view_get(self):
        """Тест GET запроса к главной странице"""
        url = reverse("reservations:home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "reservations/home.html")

        self.assertIn("home", response.context)
        self.assertIn("contacts", response.context)
        self.assertIn("services", response.context)
        self.assertIn("form", response.context)

        self.assertIsInstance(response.context["form"], FeedbackForm)

        self.assertEqual(response.context["home"], self.home)
        self.assertEqual(response.context["contacts"], self.contacts)
        self.assertEqual(len(response.context["services"]), 2)

    def test_about_view_get(self):
        """Тест GET запроса к странице 'О ресторане'"""
        url = reverse("reservations:about")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/about.html")
        self.assertIn("about", response.context)
        self.assertIn("contacts", response.context)
        self.assertIn("staff", response.context)

        self.assertEqual(response.context["about"], self.about)
        self.assertEqual(len(response.context["staff"]), 2)


class TablePagesTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(
            name="test table",
            seats=6,
        )
        self.table_2 = Table.objects.create(
            name="test table 2",
            seats=4,
        )

    def test_tables_list(self):
        url = reverse("reservations:table_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/table_list.html")
        self.assertEqual(len(response.context["tables"]), 2)
