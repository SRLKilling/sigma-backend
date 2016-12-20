from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.chat import Chat
from sigma_core.serializers.chat import ChatSerializer
from sigma_core.view.chat_member import ChatMemberViewSet


class ChatViewSet(SigmaViewSet):

    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a chat.
        """
        return self.handle_action_pk('retrieve', request, pk)

    #Method should be get or list ? There is a pk but we send a list
    @detail_route(methods=['get'])
    def list_chat_members(self, request, pk):
        """
            REST list action. Used to list the chat members of a chat that contains the user.
        """
        return serialized_response(ChatMemberSerializer, ChatMember.get_chat_members_qs(Chat.objects.get(pk=pk)))

    @detail_route(methods=['get'])
    def list_chat_messages(self,request, pk):
        """
            REST list action. Used to list the chat messages of a chat that contains the user.
        """
        return serialized_response(ChatMessageSerializer, ChatMessage.get_chat_messages_qs(Chat.objects.get(pk=pk)))


    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an chat.
            If succeeded, returns HTTP_201_CREATED with the corresponding Chat.
        """
        return self.handle_action('create', request)


    def create_post_handler(self, request, chat_serializer, chat):
        # Once a chat is created, we need to create a membership for the creator
        ChatMemberViewSet(chat=char,user=request.user).save()
