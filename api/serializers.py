from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    country = serializers.CharField()

class AttackSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    source_location = LocationSerializer()
    destination_location = LocationSerializer()
    attack_type = serializers.CharField()
    severity = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    additional_details = serializers.DictField()