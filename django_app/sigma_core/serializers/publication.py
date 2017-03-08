from sigma_api import serializers
from sigma_api.importer import load_ressource

Publication = load_ressource("Publication")

@serializers.set
class PublicationSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Publication.model
        exclude = ()
