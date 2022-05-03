from django.urls import path
from . import views


urlpatterns = [
    path("", views.reservations_page),
    path(
        "reservations/",
        views.ReservationAPIView.as_view(),
        name="reservations_api_view",
    ),
]
