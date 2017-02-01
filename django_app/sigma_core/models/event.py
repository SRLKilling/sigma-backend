from django.db import models
from sigma_api.importer import load_ressource

Participation = load_ressource("Participation")

class Event(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

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
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def events_created(user):
        return Event.objects.filter(author=user)

    @staticmethod
    def get_events(user):
    # TODO : all visible events
        events = Participation.model.objects.filter(user=user).values("event").all()
        return Event.objects.filter(pk__in=events)

    @staticmethod
    def events_interesting(user):
        events = Participation.model.objects.filter(user=user).values("event").all()
        return Event.objects.filter(pk__in=events)

    @staticmethod
    def n_events(user, n):
        return Event.events(user).order_by('date_start').all()[n:]

    @staticmethod
    def n_events_interesting(user, n):
        return Event.events_interesting(user).order_by('date_start').all()[n:]

    @staticmethod
    def events_date(user, start, end):
        return Event.events(user).filter(date_start__gte=start).filter(date_end__lte=end).all()

    @staticmethod
    def events_interesting_date(user, start, end):
        return Event.events_interesting(user).filter(date_start__gte=start).filter(date_end__lte=end).all()

    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
