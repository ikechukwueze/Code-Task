from django.core.management.base import BaseCommand
from reservations.models import Rental, Reservation


class Command(BaseCommand):
    help = "Creates rentals and reservations in database."

    def handle(self, *args, **kwargs):
        rental_names = [
            "Lakeview Homes",
            "ForestHill Apartments",
            "Destiny Court",
        ]
        for name in rental_names:
            rental = Rental.objects.create(name=name)
            res_1 = Reservation.objects.create(
                rental=rental,
                checkin="2022-01-01",
                checkout="2022-01-05",
            )
            res_2 = Reservation.objects.create(
                rental=rental,
                checkin="2022-01-07",
                checkout="2022-01-14",
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully created rentals and reservations")
        )
