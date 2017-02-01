from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

SharedPublication = load_ressource("SharedPublication")

class SharedPublicationSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        class Meta:
            model = SharedPublication.model
            exclude = ()
