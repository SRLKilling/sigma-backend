from rest_framework import serializers
from sigma_core.importer import load_ressource

SharedPublication = load_ressource("SharedPublication")


class SharedPublicationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Chat.
        Include all fields
    """
    class Meta:
        model = SharedPublication.model
        exclude = ()
