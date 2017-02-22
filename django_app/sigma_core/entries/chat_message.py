from sigma_api import entries, response
from sigma_api.importer import load_ressource

ChatMessage = load_ressource("ChatMessage")

class ChatMessageEntrySet(entries.EntrySet):

    create = entries.create()

    retrieve = entries.retrieve()
