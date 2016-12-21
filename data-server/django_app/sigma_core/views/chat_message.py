from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.chat_message import ChatMessage
from sigma_core.serializers.chat_message import ChatMessage


class ChatMessageViewSet(SigmaViewSet):

    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()

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
