from typing import Type, Union
from datetime import date
from django.db.models.base import Model
from django.core.exceptions import ValidationError
from shortuuid import ShortUUID
from .text_information import checkout_date_errmsg, reservation_conflict_errmsg


class ReservationController:
    @staticmethod
    def generate_reservation_id() -> str:
        return ShortUUID().random(length=8)

    @staticmethod
    def validate_reservation_dates(
        rental: Type[Model],
        reservation: Type[Model],
        reservation_id: str,
        checkin: date,
        checkout: date,
    ) -> Union[ValidationError, None]:

        if checkin > checkout:
            raise ValidationError(checkout_date_errmsg)

        reservation_conflict = reservation.objects.filter(
            rental=rental, checkin__lte=checkout, checkout__gte=checkin
        )

        try:
            reservation.objects.get(reservation_id=reservation_id)
        except reservation.DoesNotExist:
            # if reservation does not exist, this means
            # it is a newly created reservation object
            pass
        else:
            # else, it may be a reservation that is being
            # updated. Exclude self and check for conflicts
            reservation_conflict = reservation_conflict.exclude(
                reservation_id=reservation_id
            )

        if reservation_conflict.exists():
            raise ValidationError(reservation_conflict_errmsg)
