from sigma_api import entries, response, shortcuts
from sigma_api.importer import load_ressource

Chat = load_ressource("Chat")
ChatMessage = load_ressource("ChatMessage")
ChatMember = load_ressource("ChatMember")

class ChatEntrySet(entries.EntrySet):


    list = entries.list(
        Chat.objects.user_can_see,
        Chat.serializers.list
    )

    #What's the point of a retrieve route ?
    #retrieve = entries.retrieve()

    @entries.global_entry(bind_set=True, methods=["post"])
    def create(self, user, data):
        ''' modified to put the creator as an superadmin'''
        #Can we access easily data.group without deserializing?
        s=shortcuts.create(user, data, self.get_serializer(None), "create")
        c = Chat.objects.latest("pk")
        ChatMember.model.add_new_member_to_chat(user,c)
        return s


    #TODO : Do we really make a destroy option ??
    #destroy = entries.destroy()

    list_messages = entries.sub_list(
        sub_queryset = ChatMessage.objects.get_messages_of_chat,
        serializer = ChatMessage.serializer.default
    )

    list_members = entries.sub_list(
        sub_queryset = ChatMember.objects.get_members_of_chat,
        serializer = ChatMessage.serializer.default
    )
