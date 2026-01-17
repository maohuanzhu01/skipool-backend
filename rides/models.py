import uuid
from django.conf import settings
from django.db import models

class Destination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

class RideOffer(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "published"
        CANCELLED = "cancelled"
        COMPLETED = "completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ride_offers")
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    pickup_label = models.CharField(max_length=120)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    seats_total = models.PositiveIntegerField(default=3)
    seats_available = models.PositiveIntegerField(default=3)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)

class RideBooking(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested"
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        CANCELLED = "cancelled"
        COMPLETED = "completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ride = models.ForeignKey(RideOffer, on_delete=models.CASCADE, related_name="bookings")
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ride_bookings")
    seats_reserved = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ride", "passenger"], name="unique_booking_per_user"),
        ]
