from django.db import models
from sigma_api.importer import load_ressource
import datetime

Participation = load_ressource("Participation")

class EventQuerySet(models.QuerySet):

    def sort(self):
        return self.order_by('date_start')

    def created_by(self, user):
        return self.filter(author=user)

    def visible(self, user):
        # TODO
        return self

    def interesting(self, user):
        events = Participation.model.objects.filter(user=user).values("event")
        return self.filter(pk__in=events).order_by('date_start')

    def past(self):
        return self.filter(date_end__lte=datetime.datetime.now())

    def future(self):
        return self.filter(date_end__gte=datetime.datetime.now())

    def between(self, start, end):
        r1 = self.filter(date_start__gt=start, date_start__lt=end)
        r2 = self.filter(date_end__gt=start, date_end__lt=end)
        r3 = self.filter(date_start__lte=start, date_end__gte=end)
        return r1 | r2 | r3

class Event(models.Model):

    objects = EventQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    author = models.ForeignKey("User", related_name='created')

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1400)

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    place_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    #*********************************************************************************************#
    #**                                      Setters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def create(author, name, description, start, end, place):
        e = Event(author = author, name = name, description = description, date_start = start, date_end = end, place_name = place)
        e.save()
        return e

    def modify(name, description, start, end, place):
        e.name = name
        e.description = description
        e.date_start = start
        e.date_end = end
        e.place_name = place

    def participation(self, user, status = 0):
        # Creates if non-existent
        P = Participation.model.objects.filter(user=user, event=self)
        if P.count() > 0:
            p = P.all()[0]
            p.status = status
            p.save()
            return p
        else:
            p = Participation.model(user = user, event = self, status = status)
            p.save()
            return p

    # If a user cancels his interest, or participation
    def departicipation(self, user):
        P = Participation.model.objects.filter(user=user, event=self).delete()

    # Remove the event
    def remove(self):
        self.delete()

    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
