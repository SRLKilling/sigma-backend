from django.db import models
from sigma_core.importer import load_ressource

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
    )

    user = models.ForeignKey("User")
    event = models.ForeignKey("Event")
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
