from django.shortcuts import render # a che serve?

# Create your views here.
from rest_framework import generics, permissions
from .models import Destination, RideOffer
from .serializers import DestinationSerializer, RideOfferSerializer

class DestinationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Destination.objects.all().order_by("name")
    serializer_class = DestinationSerializer

class RideOfferListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RideOffer.objects.all().order_by("departure_time")
    serializer_class = RideOfferSerializer
