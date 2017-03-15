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

    retrieve = entries.retrieve()

    create = entries.create()

    destroy = entries.destroy()

    list_messages = entries.sub_list(
        sub_queryset = ChatMessage.objects.get_messages_of_chat,
        serializer = ChatMessage.serializer.default
    )

    list_members = entries.sub_list(
        sub_queryset = ChatMember.objects.get_members_of_chat,
        serializer = ChatMessage.serializer.default
    )
