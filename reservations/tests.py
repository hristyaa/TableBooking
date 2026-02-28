from django.test import TestCase
from django.utils import timezone
import datetime

from reservations.models import Table, Reservation
from users.models import User
from django.urls import reverse
from reservations.forms import ReservationForm

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
        start_time=timezone.now() + datetime.timedelta(hours=2)
        end_time=start_time + datetime.timedelta(hours=1)

        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            start_time=start_time,
            end_time=end_time,
            guests=4,
            status=Reservation.CONFIRMED
        )

        self.reservation_2 = Reservation.objects.create(
            user=self.user_2,
            table=self.table_2,
            start_time=start_time,
            end_time=end_time,
            guests=4,
            status=Reservation.CANCELED
        )


    def test_reservation_form_validation(self):
        """Проверка валидации формы ReservationForm"""
        self.client.login(email=self.user.email, password='1234')
        start = timezone.now() + datetime.timedelta(hours=5)
        end = start + datetime.timedelta(hours=2)
        data_invalid = {"table_id": self.table_2.id,
                "start_time": start.strftime("%Y-%m-%dT%H:%M"),
                "end_time": end.strftime("%Y-%m-%dT%H:%M"),
                "guests": 10, }

        form = ReservationForm(data=data_invalid)
        self.assertFalse(form.is_valid())
        self.assertIn("guests", form.errors)
        self.assertIn("Максимальное количество гостей за столом - 6", form.errors["guests"])
        data = {"table_id": self.table_2.id,
                        "start_time": start.strftime("%Y-%m-%dT%H:%M"),
                        "end_time": end.strftime("%Y-%m-%dT%H:%M"),
                        "guests": 6, }
        form = ReservationForm(data=data)
        self.assertTrue(form.is_valid())


    def test_create_reservation(self):
        """Тест на создание бронирования"""
        self.client.login(email=self.user_2.email, password='1234')

        url = reverse('reservations:reservation_create')
        start = timezone.now() + datetime.timedelta(hours=5)
        end = start + datetime.timedelta(hours=2)

        data = {"table_id": self.table_2.id,
            "start_time": start.strftime("%Y-%m-%dT%H:%M"),
            "end_time": end.strftime("%Y-%m-%dT%H:%M"),
            "guests": 2,}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Reservation.objects.count(), 3)
        self.assertTrue(
            Reservation.objects.filter(user=self.user_2, table=self.table_2, guests=2).exists()
        )

    def test_detail_reservation(self):
        """Тест на детальный просмотр бронирования"""
        self.client.login(email=self.user.email, password='1234')
        url = reverse('reservations:reservations_detail', args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.reservation.guests))

    # def test_reservation_update_form_validation(self):
    #     """Проверка валидации формы ReservationUpdateForm"""
    #     start = timezone.now() + datetime.timedelta(hours=2)
    #     end = start + datetime.timedelta(hours=13)
    #     data_invalid = {"table_id": self.table.id,
    #                     "start_time": start.strftime("%Y-%m-%dT%H:%M"),
    #                     "end_time": end.strftime("%Y-%m-%dT%H:%M"),
    #                     "guests": 4, }
    #
    #     form = ReservationForm(data=data_invalid)
    #     self.assertFalse(form.is_valid())
    #     self.assertIn("guests", form.errors)
    #     self.assertIn("Максимальное количество гостей за столом - 6", form.errors["guests"])
    #     data = {"table_id": self.table_2.id,
    #             "start_time": start.strftime("%Y-%m-%dT%H:%M"),
    #             "end_time": end.strftime("%Y-%m-%dT%H:%M"),
    #             "guests": 6, }
    #     form = ReservationForm(data=data)
    #     self.assertTrue(form.is_valid())



    def test_delete_reservation(self):
        """Тестирование удаления бронирования (отмены без фактического удаления, с измененим статуса)"""
        self.client.login(email=self.user.email, password='1234')
        url = reverse('reservations:reservation_delete', args=[self.reservation.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reservations:reservation_list'))

        self.assertEqual(Reservation.objects.count(), 2)
        # обновление бд для проверки статуса бронирования
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'canceled')


    def test_update_reservation(self):
        """Тестирование изменения бронирования"""
        self.client.login(email=self.user.email, password='1234')
        url = reverse('reservations:reservation_update', args=[self.reservation.id])
        start = timezone.now() + datetime.timedelta(days=2)  # +2 дня
        end = start + datetime.timedelta(hours=2)
        data = {"table": self.table_2.id,
                "start_time": start.strftime("%Y-%m-%dT%H:%M"),
                "end_time": end.strftime("%Y-%m-%dT%H:%M"),
                "guests": 2,
                }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.table.id, self.table_2.id)
        self.assertEqual(self.reservation.guests, 2)

        # проверка, что user не сможет изменить объект, созданный user_2
        url = reverse('reservations:reservation_update', args=[self.reservation_2.id])
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, 404)
        data = {"table": self.table.id,
                "start_time": start.strftime("%Y-%m-%dT%H:%M"),
                "end_time": end.strftime("%Y-%m-%dT%H:%M"),
                "guests": 4,
                }
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 404)
        self.reservation_2.refresh_from_db()
        self.assertEqual(self.reservation_2.table.id, self.table_2.id)
