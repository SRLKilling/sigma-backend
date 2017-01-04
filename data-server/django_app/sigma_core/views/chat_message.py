from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import load_ressource

ChatMessage = load_ressource("ChatMessage")


class ChatMessageViewSet(SigmaViewSet):

    serializer_class = ChatMessage.serializer
    queryset = ChatMessage.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an chat member.
            If succeeded, returns HTTP_201_CREATED with the corresponding ChatMember object.
        """
        return self.handle_action('create', request)
