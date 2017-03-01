from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Publication = load_ressource("Publication")

class PublicationSerializerSet(SerializerSet):

    class PublicationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Publication.model
            exclude = ()
