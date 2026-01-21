from math import radians, sin, cos, sqrt, atan2

from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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
