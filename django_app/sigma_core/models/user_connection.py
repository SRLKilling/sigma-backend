from django.db import models
from sigma_api.importer import load_ressource

User = load_ressource("User")
Group = load_ressource("Group")

class UserConnectionQuerySet(models.QuerySet):

    def connections_to(self,user):
        return self.filter(models.Q(user1=user) | models.Q(user2=user))

    def are_connected(self, user1, user2):
        return self.filter( (models.Q(user1=user1) and models.Q(user2=user2)) or \
                            (models.Q(user1=user2) and models.Q(user2=user1)) ).exists()

    def between_users(self, user1, user2):
        return self.get( (models.Q(user1=user1) and models.Q(user2=user2)) or \
                         (models.Q(user1=user2) and models.Q(user2=user1)) )


class UserConnection(models.Model):
    """
        This model is used to represent connections between users.
        Two users are connected when they share a group in common
    """

    objects = UserConnectionQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user1 = models.ForeignKey('User', related_name='connections2')
    user2 = models.ForeignKey('User', related_name='connections1')
    nb_of_common_groups = 1

    class Meta:
        unique_together = (("user1", "user2"),)

    def __str__(self):
        return 'Connection %d between %s and %s' % (self.pk, self.user1,self.user2)


    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#


    @staticmethod
    def create_new_connections_gr(user,group):
        """
            Create connections based on the given user and a group he just joined.
            This static method is not an API entry. It is used by others views :
            * GroupMember once someone joins a new group
        """
        group_users = User.objects.filter(group=group)
        for u in group_users:
            uc = UserConnection.objects.get_connection(user,u)
            if not uc:
                UserConnection(user1=user,user2=u).save()
            else:
                uc.nb_of_common_groups+=1


    @staticmethod
    def destroy_gr(user, group):
        """
            This static method is not an API entry. It is used by others entries :
            * GroupMember when someone quits a group
        """
        group_users = User.objects.filter(group=group)
        for u in group_users:
            uc = UserConnection.objects.get_connection(user,u)
            if uc:
                uc.nb_of_common_groups-=1
            if uc.nb_of_common_groups<=0:
                uc.destroy()
