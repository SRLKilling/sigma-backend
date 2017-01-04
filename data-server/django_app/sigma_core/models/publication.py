from django.db import models
from sigma_core.importer import load_ressource

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

    name = models.CharField(max_length=144)
    content = models.CharField(max_length=1500)

    related_event = models.ForeignKey("Event", blank=True)
    internal = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    last_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_publications_group(group):
        return Publication.model.objects.filter(group=group)

    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
