from django.db import models
from sigma_core.importer import Sigma, load_ressource

User = load_ressource("User")
Event = load_ressource("Event")

class Participation(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    POSSIBLE_STATUS = (
        (0, 'Invited'),
        (1, 'Interested'),
        (2, 'Participates'),
    )

    user = models.ForeignKey(User.model)
    event = models.ForeignKey(Event.model)
    status = models.IntegerField(choices=POSSIBLE_STATUS)

    def __str__(self):
        return self.user.email + " : " + str(self.status)

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

#    @staticmethod
#    def get_un_truc(truc):
#	return objet

    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
