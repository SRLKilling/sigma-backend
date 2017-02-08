from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Publication = load_ressource("Publication")

class PublicationSerializerSet(SerializerSet):

    class PublicationSerializer(serializers.ModelSerializer):
        """
            Basic default serializer for a Chat.
            Include all fields
        """
        class Meta:
            model = Publication.model
            exclude = ()
