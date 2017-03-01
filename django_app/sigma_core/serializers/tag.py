from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Tag = load_ressource("Tag")

class TagSerializerSet(SerializerSet):

    class TagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag.model
            exclude = ()
