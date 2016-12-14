from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response

from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.user_connection import UserConnection
from sigma_core.serializers.user_connection import UserConnectionSerializer

from sigma_core.models.user import User
from sigma_core.models.group import Group

class UserConnectionViewSet(SigmaViewSet):

    serializer_class = UserConnectionSerializer
    queryset = UserConnection.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#



    #*********************************************************************************************#
    #**                                  Write actions                                          **#
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
        group_users = User.objects.filter(group=group)
        for u in group_users:
            connection = UserConnection.objects.get(user1=user,user2=u)
            if not connection:
                connection = UserConnection.objects.get(user1=u,user2=user)
            connection.nb_of_common_groups-=1
            if connection.nb_of_common_groups<=0:
                connection.destroy()
