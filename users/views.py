from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Profile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ProfileSerializer,
    UserUpdateSerializer,
    ProfileUpdateSerializer,
)

User = get_user_model()


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserSerializer},
    description="Registra un nuovo utente normale (con o senza macchina)",
    examples=[
        OpenApiExample(
            'Esempio registrazione con auto',
            value={
                'email': 'mario.rossi@example.com',
                'password': 'SecurePass123!',
                'password_confirm': 'SecurePass123!',
                'first_name': 'Mario',
                'last_name': 'Rossi',
                'phone': '+39 333 1234567',
                'has_car': True,
                'car_model': 'Fiat Panda 4x4',
                'car_seats': 4,
                'ski_level': 'intermediate',
            },
            request_only=True,
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registra un nuovo utente normale.
    
    Crea un account utente e il profilo associato.
    Restituisce i dati utente e i token JWT per il login automatico.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Genera i token JWT
        refresh = RefreshToken.for_user(user)
        
        # Serializza l'utente creato
        user_serializer = UserSerializer(user)
        
        return Response({
            'message': 'Registrazione completata con successo!',
            'user': user_serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'message': 'Errore durante la registrazione',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer},
    description="Ottiene i dati dell'utente autenticato con il suo profilo"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Restituisce i dati dell'utente autenticato"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    request=UserUpdateSerializer,
    responses={200: UserSerializer},
    description="Aggiorna i dati base dell'utente (nome, cognome, email)"
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """Aggiorna i dati dell'utente autenticato"""
    serializer = UserUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=True,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(request.user).data)
    
    return Response({
        'message': 'Errore durante l\'aggiornamento',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ProfileUpdateSerializer,
    responses={200: ProfileSerializer},
    description="Aggiorna il profilo dell'utente autenticato"
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Aggiorna il profilo dell'utente autenticato"""
    profile = request.user.profile
    serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(ProfileSerializer(profile).data)
    
    return Response({
        'message': 'Errore durante l\'aggiornamento del profilo',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: ProfileSerializer},
    description="Ottiene il profilo pubblico di un utente tramite ID"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_public_profile(request, user_id):
    """Restituisce il profilo pubblico di un utente"""
    try:
        profile = Profile.objects.select_related('user').get(user_id=user_id)
        
        # Dati pubblici limitati
        data = {
            'id': profile.id,
            'display_name': profile.display_name,
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'has_car': profile.has_car,
            'ski_level': profile.ski_level,
            'rating_avg': profile.rating_avg,
            'rating_count': profile.rating_count,
            'rides_as_driver': profile.rides_as_driver,
            'rides_as_passenger': profile.rides_as_passenger,
            'is_verified': profile.is_verified,
            'member_since': profile.member_since_display,
        }
        
        return Response(data)
    
    except Profile.DoesNotExist:
        return Response({
            'message': 'Profilo non trovato'
        }, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Verifica se un'email è già registrata"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_email_availability(request):
    """Verifica se un'email è disponibile per la registrazione"""
    email = request.query_params.get('email', '').lower()
    
    if not email:
        return Response({
            'available': False,
            'message': 'Email non fornita'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    is_available = not User.objects.filter(email=email).exists()
    
    return Response({
        'email': email,
        'available': is_available,
        'message': 'Email disponibile' if is_available else 'Email già registrata'
    })
