from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import load_ressource

ChatMember = load_ressource("ChatMember")


class ChatMemberViewSet(SigmaViewSet):

    serializer_class = ChatMember.serializer
    queryset = ChatMember.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a chat member.
        """
        return self.handle_action_pk('retrieve', request, pk)


    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an chat member.
            If succeeded, returns HTTP_201_CREATED with the corresponding ChatMember object.
        """
        return self.handle_action('create', request)


    def destroy(self, request, pk):
        """
            REST destroy action. Used to kick a member of a chat.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        return self.handle_action_pk('destroy', request, pk)                                                                          
