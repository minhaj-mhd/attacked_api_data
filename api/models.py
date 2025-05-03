from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField,
    StringField, FloatField, IntField, DateTimeField, DictField
)

class Location(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    country = StringField(required=True, max_length=100)

class Attack(Document):
    source_location = EmbeddedDocumentField(Location, required=True)
    destination_location = EmbeddedDocumentField(Location, required=True)
    attack_type = StringField(required=True, max_length=100)
    severity = IntField(required=True)
    timestamp = DateTimeField(required=True)
    additional_details = DictField()  # To store arbitrary JSON-like details

    meta = {
        'collection': 'attacks'  # Name of the MongoDB collection
    }