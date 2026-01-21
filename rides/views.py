from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Destination, RideOffer, SkiResort
from .serializers import (
    DestinationSerializer, 
    RideOfferSerializer, 
    SkiResortSerializer,
    SkiResortSearchResultSerializer
)


def haversine_distance(lat1, lng1, lat2, lng2):
    """Calcola la distanza in km tra due punti usando la formula di Haversine"""
    R = 6371  # Raggio della Terra in km
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)
    
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


class DestinationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Destination.objects.all().order_by("name")
    serializer_class = DestinationSerializer


class RideOfferListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RideOffer.objects.all().order_by("departure_time")
    serializer_class = RideOfferSerializer


class SkiResortListView(generics.ListAPIView):
    """Lista tutti gli impianti sciistici attivi"""
    permission_classes = [permissions.AllowAny]
    queryset = SkiResort.objects.filter(is_active=True).order_by("name")
    serializer_class = SkiResortSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Testo da cercare (es: "bobio" trova "Piani di Bobbio")', required=True, type=str),
        OpenApiParameter(name='lat', description='Latitudine utente per calcolare distanza', required=False, type=float),
        OpenApiParameter(name='lng', description='Longitudine utente per calcolare distanza', required=False, type=float),
        OpenApiParameter(name='threshold', description='Soglia di similarità (0-1, default 0.4)', required=False, type=float),
    ],
    responses={200: SkiResortSearchResultSerializer(many=True)},
    description='Ricerca fuzzy degli impianti sciistici. Trova le piste anche con errori di ortografia.'
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_ski_resorts(request):
    """
    Ricerca fuzzy degli impianti sciistici.
    
    Query params:
    - q: stringa di ricerca (es: "bobio" trova "Piani di Bobbio")
    - lat: latitudine utente (per calcolare distanza)
    - lng: longitudine utente (per calcolare distanza)
    - threshold: soglia di similarità (default 0.4, range 0-1)
    
    Restituisce gli impianti trovati con:
    - distanza dall'utente (se lat/lng forniti)
    - partenze disponibili nelle vicinanze
    """
    query = request.query_params.get('q', '').strip()
    
    if not query or len(query) < 2:
        return Response(
            {"error": "Il parametro 'q' deve contenere almeno 2 caratteri"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Parametri opzionali per la posizione utente
    user_lat = request.query_params.get('lat')
    user_lng = request.query_params.get('lng')
    threshold = float(request.query_params.get('threshold', 0.4))
    
    # Esegui ricerca fuzzy
    resorts = SkiResort.fuzzy_search(query, threshold=threshold)
    
    # Se l'utente ha fornito la posizione, calcola la distanza
    if user_lat and user_lng:
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            
            # Aggiungi distanza a ogni resort
            resorts_with_distance = []
            for resort in resorts:
                distance = haversine_distance(user_lat, user_lng, resort.lat, resort.lng)
                resort.distance_km = round(distance, 1)
                resorts_with_distance.append(resort)
            
            # Ordina per distanza
            resorts = sorted(resorts_with_distance, key=lambda r: r.distance_km)
        except (ValueError, TypeError):
            pass  # Ignora errori di conversione, non calcolare distanza
    
    serializer = SkiResortSearchResultSerializer(resorts, many=True)
    
    return Response({
        "query": query,
        "count": len(resorts),
        "results": serializer.data
    })


@extend_schema(
    parameters=[
        OpenApiParameter(name='start_date', description='Data inizio (ISO 8601, es: 2026-01-22)', required=True, type=str),
        OpenApiParameter(name='end_date', description='Data fine (ISO 8601, es: 2026-01-23)', required=True, type=str),
        OpenApiParameter(name='lat', description='Latitudine utente per calcolare distanza pickup', required=False, type=float),
        OpenApiParameter(name='lng', description='Longitudine utente per calcolare distanza pickup', required=False, type=float),
        OpenApiParameter(name='ski_resort_id', description='ID impianto sciistico per filtrare', required=False, type=str),
        OpenApiParameter(name='max_distance', description='Distanza massima pickup in km', required=False, type=float),
    ],
    responses={200: RideOfferSerializer(many=True)},
    description='Cerca partenze disponibili in un range di date'
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_rides_by_date_range(request):
    """
    Cerca partenze disponibili in un range di date.
    
    Query params:
    - start_date: data inizio (ISO 8601)
    - end_date: data fine (ISO 8601)
    - lat, lng: posizione utente (opzionale)
    - ski_resort_id: filtra per impianto (opzionale)
    - max_distance: distanza massima dal pickup in km (opzionale)
    """
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')
    
    if not start_date_str or not end_date_str:
        return Response(
            {"error": "Parametri 'start_date' e 'end_date' sono obbligatori"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        
        # Se sono date senza timezone, aggiungi il timezone corrente
        if start_date.tzinfo is None:
            start_date = timezone.make_aware(start_date)
        if end_date.tzinfo is None:
            end_date = timezone.make_aware(end_date)
    except ValueError:
        return Response(
            {"error": "Formato data non valido. Usa ISO 8601 (es: 2026-01-22)"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Query base: partenze nel range di date
    rides = RideOffer.objects.filter(
        status=RideOffer.Status.PUBLISHED,
        departure_time__gte=start_date,
        departure_time__lt=end_date,
        seats_available__gt=0
    ).select_related('driver', 'destination', 'destination__ski_resort').order_by('departure_time')
    
    # Filtro opzionale per impianto sciistico
    ski_resort_id = request.query_params.get('ski_resort_id')
    if ski_resort_id:
        rides = rides.filter(destination__ski_resort_id=ski_resort_id)
    
    # Parametri posizione utente
    user_lat = request.query_params.get('lat')
    user_lng = request.query_params.get('lng')
    max_distance = request.query_params.get('max_distance')
    
    rides_list = list(rides[:50])  # Limita a 50 risultati
    
    # Se l'utente ha fornito la posizione, calcola la distanza dal pickup
    if user_lat and user_lng:
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            max_dist = float(max_distance) if max_distance else None
            
            rides_with_distance = []
            for ride in rides_list:
                distance = haversine_distance(user_lat, user_lng, ride.pickup_lat, ride.pickup_lng)
                ride.pickup_distance_km = round(distance, 1)
                
                # Filtra per distanza massima se specificata
                if max_dist is None or distance <= max_dist:
                    rides_with_distance.append(ride)
            
            # Ordina per distanza pickup
            rides_list = sorted(rides_with_distance, key=lambda r: r.pickup_distance_km)
        except (ValueError, TypeError):
            pass
    
    # Prepara la risposta
    results = []
    for ride in rides_list:
        ride_data = {
            'id': str(ride.id),
            'departure_time': ride.departure_time.isoformat(),
            'price_per_seat': float(ride.price_per_seat),
            'seats_available': ride.seats_available,
            'pickup_label': ride.pickup_label,
            'pickup_lat': ride.pickup_lat,
            'pickup_lng': ride.pickup_lng,
            'driver_name': f"{ride.driver.first_name} {ride.driver.last_name}".strip() or ride.driver.username,
            'destination': {
                'id': str(ride.destination.id),
                'name': ride.destination.name,
            }
        }
        
        # Aggiungi info ski resort se presente
        if ride.destination.ski_resort:
            ride_data['ski_resort'] = {
                'id': str(ride.destination.ski_resort.id),
                'name': ride.destination.ski_resort.name,
                'region': ride.destination.ski_resort.get_region_display(),
            }
        
        # Aggiungi distanza pickup se calcolata
        if hasattr(ride, 'pickup_distance_km'):
            ride_data['pickup_distance_km'] = ride.pickup_distance_km
        
        results.append(ride_data)
    
    return Response({
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "count": len(results),
        "results": results
    })
