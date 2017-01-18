from django.db import models
from sigma_core.importer import load_ressource

GroupMember = load_ressource("GroupMember")

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
    approved = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.publication.title

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_publications_group(group):
        return SharedPublication.objects.filter(group=group).filter(approved=True)

    def get_publications_user(user):
        membersof = GroupMember.model.get_user_memberships_qs(user).values('group')
        return SharedPublication.objects.filter(group__pk__in = membersof)


    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return True
