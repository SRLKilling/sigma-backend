from django.db import models
from sigma_core.importer import load_ressource

class Tag(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey("User", related_name="user")
    publication = models.ForeignKey("Publication")
    tagged = models.ForeignKey("User", related_name="tagged")

    def __str__(self):
        return self.user.email + " tagged " + self.tagged.email + " on " + self.publication.title

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
