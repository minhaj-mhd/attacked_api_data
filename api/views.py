# views.py
from rest_framework import views, status
from rest_framework.response import Response
from datetime import datetime
from mongoengine.queryset.visitor import Q
from .models import Attack
from .serializers import AttackSerializer


class AttackList(views.APIView):
    """
    GET /api/attacks/
    ------------------
    Returns a paginated list of all attacks with optional filtering.

    Query Parameters:
    - page (int): Page number for pagination (default: 1).
    - page_size (int): Number of records per page (default: 10).
    - start_date (ISO datetime): Filter attacks that occurred after this date.
    - end_date (ISO datetime): Filter attacks that occurred before this date.
    - attack_type (str): Filter by attack type.
    - severity (int): Filter by severity level.
    - region (str): Filter by country (case-insensitive match on source_location.country).

    Returns:
    A JSON object containing total results, pagination info, and serialized attack data.
    """
    def get(self, request, format=None):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
        except ValueError:
            page = 1
            page_size = 10
        skip = (page - 1) * page_size

        qs = Attack.objects

        # Filtering by date
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                end_dt = datetime.fromisoformat(end_date)
                qs = qs.filter(timestamp__gte=start_dt, timestamp__lte=end_dt)
            except Exception:
                return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering by attack_type, severity, region
        attack_type = request.query_params.get('attack_type')
        if attack_type:
            qs = qs.filter(attack_type__iexact=attack_type)

        severity = request.query_params.get('severity')
        if severity:
            try:
                qs = qs.filter(severity=int(severity))
            except ValueError:
                pass

        region = request.query_params.get('region')
        if region:
            qs = qs.filter(source_location__country__iexact=region)

        total = qs.count()
        attacks = qs.order_by('-timestamp')[skip:skip + page_size]
        serializer = AttackSerializer(attacks, many=True)

        data = {
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': serializer.data,
        }
        print(Response(data))
        return Response(data)


class AttackRecent(views.APIView):
    """
    GET /api/attacks/recent/
    -------------------------
    Returns a list of the most recent attacks.

    Query Parameters:
    - limit (int): Maximum number of recent attacks to return (default: 10).

    Returns:
    A list of serialized recent attack records ordered by most recent.
    """
    def get(self, request, format=None):
        try:
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            limit = 10
        qs = Attack.objects.order_by('-timestamp')[:limit]
        serializer = AttackSerializer(qs, many=True)
        return Response(serializer.data)


class AttackStatistics(views.APIView):
    """
    GET /api/attacks/statistics/
    -----------------------------
    Aggregates and returns statistics of attacks grouped by country.

    Returns:
    A dictionary where keys are country names and values are total attack counts.
    """
    def get(self, request, format=None):
        pipeline = [
            {"$group": {"_id": "$source_location.country", "total": {"$sum": 1}}}
        ]
        stats = list(Attack.objects.aggregate(*pipeline))
        response_data = {stat['_id']: stat['total'] for stat in stats}
        return Response(response_data)


class AttackVisualizationData(views.APIView):
    """
    GET /api/attacks/visualization-data/
    -------------------------------------
    Returns GeoJSON-formatted data of attacks for mapping or 3D globe visualization.

    Query Parameters:
    - view_type (str): Accepts 'map' or 'globe'; passed through in properties (default: 'map').

    Returns:
    A GeoJSON FeatureCollection containing attack location data and related properties.
    """
    def get(self, request, format=None):
        view_type = request.query_params.get('view_type', 'map')
        qs = Attack.objects.order_by('-timestamp')
        features = []

        for attack in qs:
            geometry = {
                "type": "Point",
                "coordinates": [attack.source_location.longitude, attack.source_location.latitude]
            }
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "attack_type": attack.attack_type,
                    "severity": attack.severity,
                    "timestamp": attack.timestamp.isoformat(),
                    "country": attack.source_location.country,
                    "view_type": view_type
                }
            }
            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features,
        }
        return Response(geojson)
