from sigma_api import entries, response
from sigma_api.importer import load_ressource

Chat = load_ressource("Chat")

class ChatEntrySet(entries.EntrySet):

    #TODO : create a new route to get the chat messages relative to a chat


    list = entries.list(
        Chat.objects.my_chats,
        Chat.serializers.list
    )

    retrieve = entries.retrieve()

    create = entries.create()

    destroy = entries.destroy()
