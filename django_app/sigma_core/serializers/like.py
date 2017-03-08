from sigma_api import serializers
from sigma_api.importer import load_ressource

Like = load_ressource("Like")

@serializers.set
class LikeSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Like.model
        exclude = ()
