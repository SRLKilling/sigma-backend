from sigma_api import entries, response
from sigma_api.importer import load_ressource

ChatMember = load_ressource("ChatMember")

class ChatMemberEntrySet(entries.EntrySet):


    create = entries.create()

    retrieve = entries.retrieve()

    destroy = entries.destroy()
