from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import Sigma, load_ressource

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")
Search = load_ressource("Search")
AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class SearchViewSet(SigmaViewSet):

    serializer_class = Search.serializer
    queryset = Group.model.objects.all() #to avoid errors


    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        """
            REST list action. Used to list all groups a user can see.
        """
        word = request.data["string"]
        group_qs = Group.objects.filter(name__contains = word)
        user_qs = User.objects.filter(name__contains = word)

        group_serializer = Group.serializer(group_qs,many=True)
        user_serializer = User.serializer(user_qs,many=True)
        search_serializer = Search.Serializer(user=user_serializer,group=group_serializer)
        return Response(search_serializer.data, status=status.HTTP_200_OK)

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#
