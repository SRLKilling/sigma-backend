from django.db import models
from sigma_api.importer import load_ressource


class ChatQuerySet(models.QuerySet):

    def user_can_see(self, user):
        """ QS of all the chats a user can see"""
        return self.filter(user=user)



class Chat(models.Model):
    """
        Modelize a chat
        Can be a chat of a group or not
        Can contain all members of a group or not (ex : just the prez,VP,trez) -> you can see it through chat_member
        One group at most for a chat but there can be many chats for one group (oneToMany)
        Each group has a chat, even if it's empty
    """

    objects = ChatQuerySet.as_manager()
    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    #can be null <-> in this case, it's not linked to a group
    group = models.ForeignKey('Group', related_name='chats', null=True)

    #if a chat concerns every member of a group -> no one can kicks people
    is_full_group_chat = models.BooleanField(default=False)

    # Accessible qs from ForeignKeys
    # "messages" from chat_message
    # "members" from chat_member
    # Use the methods below instead -> sorted

    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    def get_chat_messages_qs(self):


    def get_members_qs(self):
        return self.members.order_by('join_date')


    @staticmethod
    def get_group_chats_qs(group):
        return Chat.objects.filter(group=group)

    @staticmethod
    def get_user_chats(user):
        cm_list=ChatMember.objects.filter(user=user)
        return [cm.chat for cm in cm_list]

    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return user in self.get_members_qs()

    def can_list_chat_members(self,user):
        return user in self.get_members_qs()

    def can_list_chat_messages(self,user):
        return user in self.get_members_qs()
