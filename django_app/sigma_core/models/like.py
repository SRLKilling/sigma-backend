from django.db import models
from sigma_api.importer import load_ressource

class Like(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey("User")
    publication = models.ForeignKey("Publication")

    def __str__(self):
        return self.user.email + " likes " + self.publication.title

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
