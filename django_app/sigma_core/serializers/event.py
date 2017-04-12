from sigma_api import serializers
from sigma_api.importer import load_ressource

Event = load_ressource("Event")
Participation = load_ressource("Participation")

@serializers.set
class EventSerializerSet(serializers.drf.ModelSerializer):

    number_interested = serializers.drf.SerializerMethodField()
    number_invited = serializers.drf.SerializerMethodField()
    score = serializers.drf.SerializerMethodField()
    status = serializers.drf.SerializerMethodField()

    class Meta:
        model = Event.model
        fields = "__all__"

    def get_number_interested(self, event):
        return Participation.objects.for_event(event).interested().count()

    def get_number_invited(self, event):
        return Participation.objects.for_event(event).invited().count()

    def get_score(self, event):
        # TODO
        return 1

    def get_status(self, event):
        return "event"

    @serializers.sub
    class search:
        class Meta:
            fields = ('id', 'name', 'score', 'status')

