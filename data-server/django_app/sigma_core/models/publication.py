from django.db import models
from sigma_core.importer import load_ressource

SharedPublication = load_ressource("SharedPublication")

class Publication(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    group = models.ForeignKey("Group", related_name='publications')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User")

    title = models.CharField(max_length=144, blank=True)
    content = models.CharField(max_length=1500)

    related_event = models.ForeignKey("Event", blank=True, null=True)
    internal = models.BooleanField(default=True)
    last_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
