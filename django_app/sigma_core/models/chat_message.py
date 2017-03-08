from django.db import models
from sigma_api.importer import load_ressource

Chat = load_ressource("Chat")
ChatMember = load_ressource("ChatMember")

class ChatMessageQuerySet(models.QuerySet):

    def get_messages_of_chat(self, user, chat):
        return self.filter(chat=chat).order_by('created_date')

class ChatMessage(models.Model):
    """
        Modelize a message in a chat of a group
    """

    objects = ChatMessageQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey('User', related_name='my_chat_messages')
    chat = models.ForeignKey('Chat', related_name='messages')
    created_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="")


    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    #LIST VIA CHAT entry

    def can_create(self, user):
        #we need to check that the chatMessage.user is the user that sends the request
        return ChatMember.objects.is_chat_member(user, self.chat) and self.user == user
