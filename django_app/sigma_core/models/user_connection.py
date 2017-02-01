from django.db import models
from sigma_api.importer import load_ressource

User = load_ressource("User")

class UserConnection(models.Model):
    """
        This model is used to represent connections between users.
        Two users are connected when they share a group in common
    """

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
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_user_connections_qs(user):
        """
            Returns a queryset containing a user's connections
        """
        return UserConnection.objects.filter( models.Q(user1=user1) or models.Q(user2=user1) )

    @staticmethod
    def are_users_connected(user1,user2):
        """
            Returns True if user1 and user2 are connected
        """
        return UserConnection.objects.filter( models.Q(user1=user1,user2=user2) or models.Q(user1=user2,user2=user1) ).exists()



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
        group_users = User.model.objects.filter(group=group)
        for u in group_users:
            if not (UserConnection.objects.filter(user1=user,user2=u).exists() or UserConnection.objects.filter(user1=u,user2=user).exists()):
                UserConnection(user1=user,user2=u).save()
            else:
                if UserConnection.objects.filter(user1=user,user2=u).exists():
                    UserConnection.objects.filter(user1=user,user2=u).nb_of_common_groups+=1
                else:
                    UserConnection.objects.filter(user1=u,user2=user).nb_of_common_groups+=1



    @staticmethod
    def destroy_gr(user, group):
        """
            This static method is not an API entry. It is used by others views :
            * GroupMember when someone quits a group
        """
        group_users = User.model.objects.filter(group=group)
        for u in group_users:
            connection = UserConnection.objects.get(user1=user,user2=u)
            if not connection:
                connection = UserConnection.objects.get(user1=u,user2=user)
            connection.nb_of_common_groups-=1
            if connection.nb_of_common_groups<=0:
                connection.destroy()
