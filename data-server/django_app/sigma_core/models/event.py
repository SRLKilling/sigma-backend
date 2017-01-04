from django.db import models
from sigma_core.importer import load_ressource

class Event(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1400)

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    place_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

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
