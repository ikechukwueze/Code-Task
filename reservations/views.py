from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from rest_framework import generics
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer


def reservations_page(request):
    return render(request, "index.html")


class ReservationAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.select_related("rental")
    
    def list(self, request):
        query = self.get_queryset().annotate(
            previous_reservation=Subquery(
                self.get_queryset()
                .filter(rental=OuterRef('rental'))
                .exclude(checkout__gte=OuterRef('checkout'))
                .order_by('-checkout')
                .values('reservation_id')[:1]
            )
        )
        serializer = ReservationSerializer(query, many=True)
        return Response(serializer.data)