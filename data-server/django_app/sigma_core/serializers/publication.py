from rest_framework import serializers
from sigma_core.importer import load_ressource

Publication = load_ressource("Publication")


class PublicationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Chat.
        Include all fields
    """
    class Meta:
        model = Publication.model
        exclude = ()
