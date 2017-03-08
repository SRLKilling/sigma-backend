from sigma_api import serializers
from sigma_api.importer import load_ressource

Event = load_ressource("Event")

@serializers.set
class EventSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Event.model
        fields = "__all__"
