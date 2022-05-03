from typing import Union
from django.db import models
from django.core.exceptions import ValidationError
from .utils import ReservationController


class Rental(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    reservation_id = models.CharField(
        max_length=8,
        unique=True,
        default=ReservationController.generate_reservation_id,
    )
    checkin = models.DateField()
    checkout = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["rental__id", "checkout"]

    def validate_unique(self, exclude=None) -> Union[ValidationError, None]:
        super().validate_unique(exclude=exclude)

        # Ensure there are no reservation conflicts on these dates
        ReservationController.validate_reservation_dates(
            rental=self.rental,
            reservation=self.__class__,
            reservation_id=self.reservation_id,
            checkin=self.checkin,
            checkout=self.checkout,
        )

    def __str__(self) -> str:
        return self.reservation_id

    def save(self, *args, **kwargs):
        self.validate_unique()
        return super().save(*args, **kwargs)
