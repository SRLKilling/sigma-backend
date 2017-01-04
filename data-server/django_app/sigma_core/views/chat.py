from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import load_ressource

Chat = load_ressource("Chat")
ChatMember = load_ressource("ChatMember")
ChatMessage = load_ressource("ChatMessage")


class ChatViewSet(SigmaViewSet):

    serializer_class = Chat.serializer
    queryset = Chat.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a chat.
        """
        return self.handle_action_pk('retrieve', request, pk)


    @detail_route(methods=['get'])
    def list_chat_members(self, request, pk):
        """
            REST list action. Used to list the chat members of a chat that contains the user.
        """
        return serialized_response(ChatMember.serializer, ChatMember.model.get_chat_members_qs(Chat.model.objects.get(pk=pk)))

    @detail_route(methods=['get'])
    def list_chat_messages(self,request, pk):
        """
            REST list action. Used to list the chat messages of a chat that contains the user.
        """
        return serialized_response(ChatMessage.serializer, ChatMessage.model.get_chat_messages_qs(Chat.model.objects.get(pk=pk)))


    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create a chat.
            If succeeded, returns HTTP_201_CREATED with the corresponding Chat.
        """
        return self.handle_action('create', request)


    def create_post_handler(self, request, chat_serializer, chat):
        # Once a chat is created, we need to create a membership for the creator
        # ChatMember.view.(chat=char,user=request.user).save()
        # WTF is this line ?
        pass
