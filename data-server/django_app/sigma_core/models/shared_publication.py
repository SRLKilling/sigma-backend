from django.db import models
from sigma_core.importer import Sigma, load_ressource

load_ressource("Publication")
load_ressource("Group")

class SharedPublication(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    publication = models.ForeignKey(Sigma.Publication.model, related_name='shared')
    group = models.ForeignKey(Sigma.Group.model, related_name='shared_publications')
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.publication.name

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
