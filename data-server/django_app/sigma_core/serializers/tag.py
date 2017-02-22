from rest_framework import serializers
from sigma_core.importer import load_ressource

Tag = load_ressource("Tag")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag.model
        exclude = ()
