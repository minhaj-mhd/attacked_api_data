from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    """
    Serializer for the Location embedded document.

    Fields:
    - latitude (float): Latitude coordinate of the location.
    - longitude (float): Longitude coordinate of the location.
    - country (str): Name of the country associated with the location.
    """
    latitude = serializers.FloatField(help_text="Latitude coordinate of the location.")
    longitude = serializers.FloatField(help_text="Longitude coordinate of the location.")
    country = serializers.CharField(help_text="Country name associated with the location.")


class AttackSerializer(serializers.Serializer):
    """
    Serializer for the Attack document.

    Fields:
    - id (str): Unique identifier for the attack (read-only).
    - source_location (LocationSerializer): Origin location of the attack.
    - destination_location (LocationSerializer): Target location of the attack.
    - attack_type (str): Type of the cyber attack (e.g., DDoS, Phishing).
    - severity (int): Numeric indicator of the attack's severity.
    - timestamp (datetime): Timestamp of when the attack occurred.
    - additional_details (dict): Optional metadata or context about the attack.
    """
    id = serializers.CharField(read_only=True, help_text="Unique identifier for the attack.")
    source_location = LocationSerializer(help_text="Origin location of the attack.")
    destination_location = LocationSerializer(help_text="Target location of the attack.")
    attack_type = serializers.CharField(help_text="Type or category of the cyber attack.")
    severity = serializers.IntegerField(help_text="Severity level of the attack (e.g., 1–10).")
    timestamp = serializers.DateTimeField(help_text="Date and time when the attack occurred.")
    additional_details = serializers.DictField(help_text="Arbitrary key-value pairs with additional details.")
