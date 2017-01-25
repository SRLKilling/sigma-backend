from rest_framework import serializers
from sigma_core.importer import load_ressource

SharedPublication = load_ressource("SharedPublication")

class SharedPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedPublication.model
        exclude = ()
