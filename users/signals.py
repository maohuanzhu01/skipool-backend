from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Crea automaticamente un profilo quando viene creato un utente"""
    if created:
        # Controlla se il profilo non esiste già (potrebbe essere stato creato nel serializer)
        if not hasattr(instance, 'profile') or not Profile.objects.filter(user=instance).exists():
            display_name = f"{instance.first_name} {instance.last_name}".strip() or instance.username
            Profile.objects.create(user=instance, display_name=display_name)
