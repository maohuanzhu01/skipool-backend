import uuid
from django.conf import settings
from django.db import models
from difflib import SequenceMatcher


class SkiResort(models.Model):
    """
    Tabella di dominio per gli impianti sciistici in Italia e dintorni.
    Supporta la ricerca fuzzy per trovare le piste anche con errori di ortografia.
    """
    class Region(models.TextChoices):
        LOMBARDIA = "lombardia", "Lombardia"
        PIEMONTE = "piemonte", "Piemonte"
        VALLE_AOSTA = "valle_aosta", "Valle d'Aosta"
        TRENTINO = "trentino", "Trentino-Alto Adige"
        VENETO = "veneto", "Veneto"
        FRIULI = "friuli", "Friuli-Venezia Giulia"
        EMILIA = "emilia", "Emilia-Romagna"
        TOSCANA = "toscana", "Toscana"
        ABRUZZO = "abruzzo", "Abruzzo"
        SVIZZERA = "svizzera", "Svizzera"
        FRANCIA = "francia", "Francia"
        AUSTRIA = "austria", "Austria"
        SLOVENIA = "slovenia", "Slovenia"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, db_index=True)
    # Nomi alternativi per la ricerca fuzzy (es: "Bobbio, Piani Bobbio, Valsassina")
    alternative_names = models.TextField(blank=True, help_text="Nomi alternativi separati da virgola")
    region = models.CharField(max_length=20, choices=Region.choices)
    province = models.CharField(max_length=50, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    altitude_min = models.PositiveIntegerField(null=True, blank=True, help_text="Altitudine minima in metri")
    altitude_max = models.PositiveIntegerField(null=True, blank=True, help_text="Altitudine massima in metri")
    km_slopes = models.PositiveIntegerField(null=True, blank=True, help_text="Km di piste")
    lifts_count = models.PositiveIntegerField(null=True, blank=True, help_text="Numero di impianti di risalita")
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Impianto Sciistico"
        verbose_name_plural = "Impianti Sciistici"

    def __str__(self):
        return f"{self.name} ({self.get_region_display()})"

    @property
    def all_searchable_names(self):
        """Restituisce tutti i nomi ricercabili (nome principale + alternativi)"""
        names = [self.name.lower()]
        if self.alternative_names:
            names.extend([n.strip().lower() for n in self.alternative_names.split(",")])
        return names

    @classmethod
    def fuzzy_search(cls, query, threshold=0.5):
        """
        Ricerca fuzzy che trova le piste anche con errori di ortografia.
        Es: "bobio" -> "Piani di Bobbio"
        """
        query_lower = query.lower().strip()
        results = []
        
        for resort in cls.objects.filter(is_active=True):
            best_score = 0
            for searchable_name in resort.all_searchable_names:
                # Calcola similarità con SequenceMatcher
                score = SequenceMatcher(None, query_lower, searchable_name).ratio()
                
                # Bonus se la query è contenuta nel nome o viceversa
                if query_lower in searchable_name or searchable_name in query_lower:
                    score = max(score, 0.8)
                
                # Bonus per match parziale delle parole
                query_words = set(query_lower.split())
                name_words = set(searchable_name.split())
                common_words = query_words & name_words
                if common_words:
                    word_score = len(common_words) / max(len(query_words), len(name_words))
                    score = max(score, word_score * 0.9)
                
                best_score = max(best_score, score)
            
            if best_score >= threshold:
                results.append((resort, best_score))
        
        # Ordina per score decrescente
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results]


class Destination(models.Model):
    """Manteniamo per retrocompatibilità, ma ora punta a SkiResort"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    # Collegamento opzionale a SkiResort
    ski_resort = models.ForeignKey(SkiResort, on_delete=models.SET_NULL, null=True, blank=True)

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
