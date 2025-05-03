# views.py
from rest_framework import views, status
from rest_framework.response import Response
from datetime import datetime
from mongoengine.queryset.visitor import Q
from .models import Attack
from .serializers import AttackSerializer

# 1. GET /api/attacks/ : List all attacks with pagination and filtering
class AttackList(views.APIView):
    def get(self, request, format=None):
        # Handle pagination
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
        except ValueError:
            page = 1
            page_size = 10
        skip = (page - 1) * page_size

        qs = Attack.objects

        # Filtering by date (using ISO date format, e.g., 2025-05-01T09:23:00)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                end_dt = datetime.fromisoformat(end_date)
                qs = qs.filter(timestamp__gte=start_dt, timestamp__lte=end_dt)
            except Exception as e:
                return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering by simple fields
        attack_type = request.query_params.get('attack_type')
        if attack_type:
            qs = qs.filter(attack_type=attack_type)
        severity = request.query_params.get('severity')
        if severity:
            try:
                qs = qs.filter(severity=int(severity))
            except ValueError:
                pass
        # Assuming filtering by region (using source_location.country)
        region = request.query_params.get('region')
        if region:
            qs = qs.filter(source_location__country__iexact=region)

        total = qs.count()
        attacks = qs.order_by('-timestamp')[skip:skip+page_size]
        serializer = AttackSerializer(attacks, many=True)
        data = {
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': serializer.data,
        }
        return Response(data)
# 2. GET /api/attacks/recent/ : Return the most recent attacks (limit is configurable)
class AttackRecent(views.APIView):
    def get(self, request, format=None):
        try:
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            limit = 10
        qs = Attack.objects.order_by('-timestamp')[:limit]
        serializer = AttackSerializer(qs, many=True)
        return Response(serializer.data)

# 3. GET /api/attacks/statistics/ : Aggregate and return attack statistics by country/region
class AttackStatistics(views.APIView):
    def get(self, request, format=None):
        # Use MongoEngine's aggregation pipeline to group by source_location.country
        pipeline = [
            {"$group": {"_id": "$source_location.country", "total": {"$sum": 1}}}
        ]
        stats = list(Attack.objects.aggregate(*pipeline))
        # Format the results in a dictionary
        response_data = { stat['_id']: stat['total'] for stat in stats }
        return Response(response_data)

# 4. GET /api/attacks/visualization-data/ : Return GeoJSON-formatted data
class AttackVisualizationData(views.APIView):
    def get(self, request, format=None):
        view_type = request.query_params.get('view_type', 'map')  # Accepts "map" or "globe"
        qs = Attack.objects.order_by('-timestamp')
        features = []
        for attack in qs:
            geometry = {
                "type": "Point",
                # Using the source_location's coordinates for visualization:
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
                    "view_type": view_type  # Pass through for client-side optimization if needed
                }
            }
            features.append(feature)
        geojson = {
            "type": "FeatureCollection",
            "features": features,
        }
        return Response(geojson)