from rest_framework import serializers
from sigma_core.importer import load_ressource

Event = load_ressource("Event")

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event.model
        exclude = ()
