from django.db import models
from sigma_api.importer import load_ressource

class ParticipationQuerySet(models.QuerySet):

    def invited(self):
        return self.filter(POSSIBLE_STATUS = 0)

    def interested(self):
        return self.filter(POSSIBLE_STATUS = 1)

   def for_user(self, user):
       return self.filter(user = user)

    def for_event(self, event):
        return self.filter(event = event)

class Participation(models.Model):

    objects = ParticipationQuerySet.as_manager()

    POSSIBLE_STATUS = (
        (0, 'Invited'),
        (1, 'Interested'),
    )

    user = models.ForeignKey("User")
    event = models.ForeignKey("Event")
    status = models.IntegerField(choices=POSSIBLE_STATUS)

    def __str__(self):
        return "Participation(" + ", ".join([self.user.__str__(), self.event.__str__(), self.status]) + ")"

   def can_retrieve(self, user):
        return True
