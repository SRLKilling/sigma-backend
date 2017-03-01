from sigma_api import entries, response
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

    @entries.detailed_entry(methods=["post"])
    def list_messages(user, data, pk):
        qs = ChatMessage.get_messages_of_chat(pk)
        return shortcuts.list(user, data, qs, ChatMessage.serializer.default)

    @entries.detailed_entry(methods=["post"])
    def list_members(user, data, pk):
        qs = ChatMember.get_members_of_chat(pk)
        return shortcuts.list(user, data, qs, ChatMember.serializer.default)
