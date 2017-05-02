from sigma_api import serializers
from sigma_api.importer import load_ressource
from django.utils import timezone
import datetime

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
        #the score relies on the number of people interested by the event,
        #and whether the event is upcoming
        #0.5 for the number of people interested
        #0.5 for the date
        number_interested = Participation.objects.for_event(event).interested().count()

        equiv = [0,0.3,0.5,0.6,0.7,0.8,0.8,0.8,0.9,0.9]

        score = 0.25
        if number_interested//100<1000:
            score = equiv[number_interested//100]

        if event.date_end-datetime.timedelta(days=3)<=timezone.now(): #increase if it's coming
            score+=0.5
        elif event.date_end-datetime.timedelta(days=7)<=timezone.now():
            score+=0.25
        return score

    def get_status(self, event):
        return "event"

    @serializers.sub
    class search:
        class Meta:
            fields = ('id', 'name', 'score', 'status')
