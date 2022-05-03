from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    rental = serializers.CharField()
    previous_reservation = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        exclude = ["id", "created_at"]
        read_only_fields = ["reservation_id"]

    def get_previous_reservation(self, obj):
        previous_reservation = (
            Reservation.objects.filter(rental=obj.rental)
            .exclude(checkout__gte=obj.checkout)
            .order_by("checkout")
            .last()
        )

        if previous_reservation:
            return previous_reservation.reservation_id
        return "-"
