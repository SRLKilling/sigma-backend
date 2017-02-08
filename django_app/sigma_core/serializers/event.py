from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Event = load_ressource("Event")

class EventSerializerSet(SerializerSet):

    class EventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event.model
            exclude = ()
