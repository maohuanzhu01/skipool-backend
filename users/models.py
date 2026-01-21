from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Profilo esteso dell'utente"""
    
    class ProfileType(models.TextChoices):
        NORMAL = 'normal', 'Utente Normale'
        TRAVEL_AGENCY = 'travel_agency', 'Agenzia Viaggio'
        ASSOCIATION = 'association', 'Associazione'
        SPECIAL = 'special', 'Special'
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=80)
    photo_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    
    # Tipo di profilo
    profile_type = models.CharField(
        max_length=20,
        choices=ProfileType.choices,
        default=ProfileType.NORMAL
    )
    
    # Informazioni di contatto
    phone = models.CharField(max_length=20, blank=True)
    
    # Info specifiche per utenti normali
    has_car = models.BooleanField(default=False, help_text="L'utente ha una macchina disponibile")
    car_model = models.CharField(max_length=100, blank=True, help_text="Modello dell'auto")
    car_seats = models.PositiveSmallIntegerField(default=4, help_text="Posti disponibili in auto")
    
    # Preferenze sci
    ski_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Principiante'),
            ('intermediate', 'Intermedio'),
            ('advanced', 'Avanzato'),
            ('expert', 'Esperto'),
        ],
        blank=True
    )
    favorite_resorts = models.ManyToManyField('rides.SkiResort', blank=True, related_name='fans')
    
    # Statistiche e reputazione
    rating_avg = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    rides_as_driver = models.PositiveIntegerField(default=0)
    rides_as_passenger = models.PositiveIntegerField(default=0)
    
    # Social
    instagram_handle = models.CharField(max_length=50, blank=True)
    
    # Date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Verifiche
    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name or self.user.username
    
    @property
    def total_rides(self):
        return self.rides_as_driver + self.rides_as_passenger
    
    @property
    def member_since_display(self):
        return self.created_at.strftime("%B %Y")
