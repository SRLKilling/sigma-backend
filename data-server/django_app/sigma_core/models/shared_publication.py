from django.db import models
from sigma_core.importer import load_ressource

class SharedPublication(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    # Liste des champs de l'objet
    publication = models.ForeignKey("Publication", related_name='shared')
    group = models.ForeignKey("Group", related_name='shared_publications')
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
