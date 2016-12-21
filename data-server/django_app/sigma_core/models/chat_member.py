from django.db import models
from sigma_core.models.group import Group
from sigma_core.models.chat import Chat

class ChatMember(models.Model):
    """
        Modelize the relation bewteen a chat and a user
    """

    class Meta:
        unique_together = (("user", "chat"),)


    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    user = models.ForeignKey('User', related_name='chats')
    chat = models.ForeignKey('Chat', related_name='members')
    join_date = models.DateTimeField(auto_now_add=True)

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#


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
