from datetime import date, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Rental, Reservation
from rest_framework.test import APITestCase
from .text_information import checkout_date_errmsg, reservation_conflict_errmsg
from .utils import ReservationController


class RentalTestCase(TestCase):
    def setUp(self):
        self.rental_name = "Westview Home"
        self.rental = Rental.objects.create(name=self.rental_name)

    def test_create_rental(self):
        self.assertEqual(Rental.objects.exists(), True)
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(Rental.objects.get(pk=1).name, self.rental_name)


class ReservationTestCase(TestCase):
    def setUp(self):
        self.rental_name = "Westview Home"
        self.checkin_date = date.today()
        self.checkout_date = self.checkin_date + timedelta(days=3)
        self.rental = Rental.objects.create(name=self.rental_name)
        self.reservation = Reservation.objects.create(
            rental=self.rental,
            checkin=self.checkin_date,
            checkout=self.checkout_date,
        )

    def test_create_reservation(self):
        self.assertEqual(Reservation.objects.exists(), True)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get(pk=1).rental, self.rental)
        self.assertIsNotNone(Reservation.objects.get(pk=1).reservation_id)
        self.assertEqual(
            Reservation.objects.get(pk=1).checkin, self.checkin_date
        )
        self.assertEqual(
            Reservation.objects.get(pk=1).checkout, self.checkout_date
        )

    def test_wrong_checkin_checkout_date(self):
        with self.assertRaises(ValidationError) as err:
            Reservation.objects.create(
                rental=self.rental,
                checkin=self.checkin_date + timedelta(days=2),
                checkout=self.checkin_date,
            )
        self.assertEqual(err.exception.message, checkout_date_errmsg)

    def test_reservation_conflict(self):
        with self.assertRaises(ValidationError) as err:
            Reservation.objects.create(
                rental=self.rental,
                checkin=self.checkin_date,
                checkout=self.checkin_date + timedelta(days=2),
            )
        self.assertEqual(err.exception.message, reservation_conflict_errmsg)


class ReservationViewTestCase(TestCase):
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class ReservationApiTestCase(APITestCase):
    fixtures = ["rentals.json", "reservations.json"]

    def setUp(self):
        url = reverse("reservations_api_view")
        self.response = self.client.get(url)

    def test_get_reservations_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), len(self.response.data))


class ReservationApiTestCase2(APITestCase):
    fixtures = ["rentals.json", "reservations_extra.json"]

    def setUp(self):
        url = reverse("reservations_api_view")
        self.response = self.client.get(url)

    def test_previous_reservation_field_in_response(self):
        resp = self.response.data
        reservation_ids = Reservation.objects.values("reservation_id")

        self.assertEqual(resp[0]["previous_reservation"], "-")

        for index in range(1, len(resp)):
            self.assertEqual(
                resp[index]["previous_reservation"],
                reservation_ids[index - 1]["reservation_id"],
            )


class ReservationIdTestCase(TestCase):
    def setUp(self):
        n = 100000
        self.reservation_id_list = [
            ReservationController.generate_reservation_id() for i in range(n)
        ]

    def test_no_duplicate_reservation_id(self):
        self.assertEqual(
            len(self.reservation_id_list), len(set(self.reservation_id_list))
        )
