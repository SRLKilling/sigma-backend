from django.db import models
from sigma_api.importer import load_ressource

Chat = load_ressource("Chat")

class ChatMessageQuerySet(models.QuerySet):

    def get_messages_of_chat(self, chat):
        return self.filter(chat=chat).order_by(created_date)

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
    message = models.TextFIeld(Defaul="")



    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_group_chat_messages_qs(group):
        c_list = Chat.model.objects.get(group=group)
        return c_list.order_by('created_date')



    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def can_create(self, user):
        return user in self.chat.get_members_qs()
