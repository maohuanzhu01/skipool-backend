from django.contrib import admin
from .models import SkiResort, Destination, RideOffer, RideBooking


@admin.register(SkiResort)
class SkiResortAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'province', 'km_slopes', 'lifts_count', 'is_active']
    list_filter = ['region', 'is_active']
    search_fields = ['name', 'alternative_names', 'province']
    ordering = ['name']
    fieldsets = (
        ('Informazioni base', {
            'fields': ('name', 'alternative_names', 'region', 'province', 'is_active')
        }),
        ('Posizione', {
            'fields': ('lat', 'lng')
        }),
        ('Caratteristiche', {
            'fields': ('altitude_min', 'altitude_max', 'km_slopes', 'lifts_count', 'website')
        }),
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'subtitle', 'ski_resort']
    search_fields = ['name']
    list_filter = ['ski_resort']


@admin.register(RideOffer)
class RideOfferAdmin(admin.ModelAdmin):
    list_display = ['driver', 'destination', 'departure_time', 'price_per_seat', 'seats_available', 'status']
    list_filter = ['status', 'departure_time']
    search_fields = ['driver__username', 'destination__name']


@admin.register(RideBooking)
class RideBookingAdmin(admin.ModelAdmin):
    list_display = ['ride', 'passenger', 'seats_reserved', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['passenger__username']
