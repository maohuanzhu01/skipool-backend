from rest_framework import serializers
from .models import Destination, RideOffer, SkiResort


class SkiResortSerializer(serializers.ModelSerializer):
    region_display = serializers.CharField(source='get_region_display', read_only=True)
    
    class Meta:
        model = SkiResort
        fields = [
            "id", "name", "alternative_names", "region", "region_display",
            "province", "lat", "lng", "altitude_min", "altitude_max",
            "km_slopes", "lifts_count", "website", "is_active"
        ]


class SkiResortSearchResultSerializer(serializers.ModelSerializer):
    """Serializer per i risultati di ricerca con distanza e partenze"""
    region_display = serializers.CharField(source='get_region_display', read_only=True)
    distance_km = serializers.FloatField(read_only=True, required=False)
    available_rides = serializers.SerializerMethodField()
    
    class Meta:
        model = SkiResort
        fields = [
            "id", "name", "region", "region_display", "province",
            "lat", "lng", "altitude_min", "altitude_max", "km_slopes",
            "distance_km", "available_rides"
        ]
    
    def get_available_rides(self, obj):
        """Restituisce le partenze disponibili per questo impianto"""
        from django.utils import timezone
        
        # Prende le partenze future per questa destinazione
        rides = RideOffer.objects.filter(
            destination__ski_resort=obj,
            status=RideOffer.Status.PUBLISHED,
            departure_time__gte=timezone.now(),
            seats_available__gt=0
        ).select_related('driver', 'destination').order_by('departure_time')[:5]
        
        return [{
            'id': str(ride.id),
            'departure_time': ride.departure_time.isoformat(),
            'price_per_seat': float(ride.price_per_seat),
            'seats_available': ride.seats_available,
            'pickup_label': ride.pickup_label,
            'pickup_lat': ride.pickup_lat,
            'pickup_lng': ride.pickup_lng,
            'driver_name': f"{ride.driver.first_name} {ride.driver.last_name}".strip() or ride.driver.username
        } for ride in rides]


class DestinationSerializer(serializers.ModelSerializer):
    ski_resort = SkiResortSerializer(read_only=True)
    
    class Meta:
        model = Destination
        fields = ["id", "name", "subtitle", "lat", "lng", "ski_resort"]


class RideOfferSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()
    driver_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RideOffer
        fields = [
            "id", "driver", "driver_name", "destination", "departure_time", 
            "pickup_label", "pickup_lat", "pickup_lng", "price_per_seat", 
            "seats_available", "status"
        ]
    
    def get_driver_name(self, obj):
        return f"{obj.driver.first_name} {obj.driver.last_name}".strip() or obj.driver.username
