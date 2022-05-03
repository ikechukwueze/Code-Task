from django.shortcuts import render
from rest_framework import generics
from .models import Reservation
from .serializers import ReservationSerializer


def reservations_page(request):
    return render(request, "index.html")


class ReservationAPIView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
