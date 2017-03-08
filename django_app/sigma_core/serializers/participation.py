from sigma_api import serializers
from sigma_api.importer import load_ressource

Participation = load_ressource("Participation")

@serializers.set
class ParticipationSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Participation.model
        exclude = ()
