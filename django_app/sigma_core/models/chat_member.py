from django.db import models
from sigma_api.importer import load_ressource

class ChatMemberQuerySet(models.QuerySet):

    def get_members_of_chat(self, chat):
        return self.filter(chat=chat).order_by(join_date)


class ChatMember(models.Model):
    """
        Modelize the relation bewteen a chat and a user
    """

    class Meta:
        unique_together = (("user", "chat"),)

    objects = ChatMemberQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey('User', related_name='chats')
    chat = models.ForeignKey('Chat', related_name='members')
    join_date = models.DateTimeField(auto_now_add=True)

    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    #can't destroy if it's the chat of a whole group -> chat.is_full_group_chat

    def can_retrieve(self, user):
        return user in self.chat.get_members_qs()

    def can_destroy(self, user):
        return user in self.chat.get_members_qs() and (not self.chat.is_full_group_chat or not self.chat.group)

    def can_create(self, user):
        # with the unique_together we're sure that you can't add someone that's already in the group
        return user in self.chat.get_members_qs() and (not self.chat.is_full_group_chat or not self.chat.group)
