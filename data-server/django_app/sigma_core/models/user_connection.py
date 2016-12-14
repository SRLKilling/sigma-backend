from django.db import models

class UserConnection(models.Model):
    """
        This model is used to represent connections between users.
        Two users are connected when they share a group in common
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user1 = models.ForeignKey('User', related_name='connections')
    user2 = models.ForeignKey('User', related_name='connections')
    nb_of_common_groups = 1

    class Meta:
        unique_together = (("user1", "user2"),)

    def __str__(self):
        return 'Connection %d between %s and %s' % (self.pk, self.user1,self.user2)




    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_users_connected_to(user):
        """
            Returns a list containing the users who are connected to user
        """
        if type(user)!=int:
            user=user.pk

        l=[]
        for c in user.connections:
            if c.user1!=user:
                l.append(user1)
            else:
                l.append(user2)
        return l

    @staticmethod
    def are_users_connected(user1,user2):
        """
            Returns True if user1 and user2 are connected
        """
        if type(user1)!=int:
            user1=user1.pk
        if type(user1)!=int:
            user2=user2.pk

        return UserConnection.all().filter(user1=user1,user2=user2).exists() or UserConnection.all().filter(user1=user2,user2=user1).exists()



    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#
