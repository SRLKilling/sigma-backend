from sigma_api import serializers
from sigma_api.importer import load_ressource

Tag = load_ressource("Tag")

@serializers.set
class TagSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Tag.model
        exclude = ()
