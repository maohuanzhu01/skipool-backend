from rest_framework import serializers
from .models import Destination, RideOffer

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "name", "subtitle", "lat", "lng"]

class RideOfferSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()
    class Meta:
        model = RideOffer
        fields = ["id", "driver", "destination", "departure_time", "pickup_label",
                  "pickup_lat", "pickup_lng", "price_per_seat", "seats_available", "status"]
