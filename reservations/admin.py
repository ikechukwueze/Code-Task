from django.contrib import admin
from .models import Rental, Reservation


class RentalAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "rental",
        "reservation_id",
        "checkin",
        "checkout",
        "created_at",
    ]
    readonly_fields = ["reservation_id"]
    search_fields = ["rental__name", "reservation_id"]


admin.site.register(Rental, RentalAdmin)
admin.site.register(Reservation, ReservationAdmin)
