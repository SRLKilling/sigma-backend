from django.db import models
from sigma_api.importer import load_ressource

ChatMember = load_ressource("ChatMember")
Chat = load_ressource("Chat")

class ChatMemberQuerySet(models.QuerySet):

    def get_members_of_chat(self, user, chat):
        return self.filter(chat=chat).order_by('join_date')

    def is_chat_member(self, user, chat):
        return self.filter(user=user, chat=chat).exists()

    def are_connected(self, user1, user2):
        """ Return True if both users are members of at least one common chat """
        chat1 = Chat.objects.filter(members__user = user1)
        return self.filter(user=user2, chat = chat1).exists()


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


    @staticmethod
    def add_new_member(user,group):
        """
            add a new member to a chat linked to a group
        """
        c = Chat.objects.get(is_full_group_chat=True, group=group)
        try:
            ChatMember(user=user,chat=c).save()
        except c.DoesNotExist:
            print("Error : no chat with this group")


    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    #can't destroy if it's the chat of a whole group -> chat.is_full_group_chat

    #LIST VIA CHAT

    def can_retrieve(self, user):
        return ChatMember.objects.is_chat_member(user, self.chat)

    def can_destroy(self, user):
        return ChatMember.objects.is_chat_member(user, self.chat) and (not self.chat.is_full_group_chat or not self.chat.group)

    def can_create(self, user):
        # with the unique_together we're sure that you can't add someone that's already in the group
        return ChatMember.objects.is_chat_member(user, self.chat) and (not self.chat.is_full_group_chat or not self.chat.group)
