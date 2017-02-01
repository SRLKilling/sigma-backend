from django.db import models
from sigma_core.importer import load_ressource

class Comment(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey("User")
    publication = models.ForeignKey("Publication")
    comment = models.CharField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + " : " + self.publication.title

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
