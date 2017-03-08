from django.db import models
from sigma_api.importer import load_ressource

Chat = load_ressource("Chat")
ChatMember = load_ressource("ChatMember")

class ChatQuerySet(models.QuerySet):

    def user_can_see(self, user):
        """ QS of all the chats a user can see"""
        chat_pks = ChatMember.objects.filter(user=user).values("chat")
        return self.filter(pk__in = chat_pks)



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

    @staticmethod
    def create_chat(group):
        """
            Create a chat based on the given group.
        """
        Chat.model(is_full_group_chat=True, group=group).save()

    @property
    def number_of_members(self):
        return ChatMember.objects.filter(chat=self).count()


    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        return ChatMember.objects.is_chat_member(user, self)

    def can_list_chat_members(self,user):
        return ChatMember.objects.is_chat_member(user, self)

    def can_list_chat_messages(self,user):
        return ChatMember.objects.is_chat_member(user, self)

    def can_list(self, user):
        return True
