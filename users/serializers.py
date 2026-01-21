from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer per il profilo utente"""
    
    member_since = serializers.CharField(source='member_since_display', read_only=True)
    total_rides = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'display_name',
            'photo_url',
            'bio',
            'profile_type',
            'phone',
            'has_car',
            'car_model',
            'car_seats',
            'ski_level',
            'rating_avg',
            'rating_count',
            'rides_as_driver',
            'rides_as_passenger',
            'total_rides',
            'instagram_handle',
            'is_verified',
            'is_phone_verified',
            'member_since',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'rating_avg', 
            'rating_count', 
            'rides_as_driver', 
            'rides_as_passenger',
            'is_verified',
            'is_phone_verified',
            'created_at',
            'updated_at',
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer per l'utente con profilo incluso"""
    
    profile = ProfileSerializer(read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_type',
            'profile',
            'date_joined',
        ]
        read_only_fields = ['date_joined']


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer per la registrazione di nuovi utenti"""
    
    # Campi User
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    
    # Campi Profile
    display_name = serializers.CharField(required=False, max_length=80, allow_blank=True)
    phone = serializers.CharField(required=False, max_length=20, allow_blank=True)
    has_car = serializers.BooleanField(required=False, default=False)
    car_model = serializers.CharField(required=False, max_length=100, allow_blank=True)
    car_seats = serializers.IntegerField(required=False, default=4, min_value=1, max_value=9)
    bio = serializers.CharField(required=False, max_length=500, allow_blank=True)
    ski_level = serializers.ChoiceField(
        required=False,
        choices=[
            ('beginner', 'Principiante'),
            ('intermediate', 'Intermedio'),
            ('advanced', 'Avanzato'),
            ('expert', 'Esperto'),
        ],
        allow_blank=True
    )
    
    def validate_email(self, value):
        """Verifica che l'email non sia già in uso"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Questa email è già registrata.")
        return value.lower()
    
    def validate(self, attrs):
        """Verifica che le password corrispondano"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Le password non corrispondono."
            })
        return attrs
    
    def create(self, validated_data):
        """Crea l'utente e il profilo associato"""
        # Estrai i dati del profilo
        profile_data = {
            'display_name': validated_data.pop('display_name', ''),
            'phone': validated_data.pop('phone', ''),
            'has_car': validated_data.pop('has_car', False),
            'car_model': validated_data.pop('car_model', ''),
            'car_seats': validated_data.pop('car_seats', 4),
            'bio': validated_data.pop('bio', ''),
            'ski_level': validated_data.pop('ski_level', ''),
            'profile_type': 'normal',  # Default per utenti normali
        }
        
        # Rimuovi password_confirm
        validated_data.pop('password_confirm')
        
        # Crea l'utente (usa il modello User standard di Django)
        user = User.objects.create_user(
            username=validated_data['email'],  # Usa email come username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        # Se display_name non è fornito, usa nome + cognome
        if not profile_data['display_name']:
            profile_data['display_name'] = f"{user.first_name} {user.last_name}"
        
        # Crea il profilo
        Profile.objects.create(user=user, **profile_data)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer per aggiornare i dati utente"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def validate_email(self, value):
        """Verifica che l'email non sia già in uso da altri"""
        user = self.context.get('request').user
        if User.objects.filter(email=value.lower()).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Questa email è già in uso.")
        return value.lower()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer per aggiornare il profilo"""
    
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'photo_url',
            'bio',
            'phone',
            'has_car',
            'car_model',
            'car_seats',
            'ski_level',
            'instagram_handle',
        ]
