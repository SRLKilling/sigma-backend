from rest_framework import serializers
from sigma_core.importer import load_ressource

Publication = load_ressource("Publication")

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication.model
        exclude = ()
