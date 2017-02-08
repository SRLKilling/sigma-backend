from sigma_api import entries, response
from sigma_api.importer import load_ressource

ChatMember = load_ressource("ChatMember")

class ChatMemberEntrySet(entries.EntrySet):


    create = entries.create()

    #TODO : route which list chatmembers of a particular chat

    retrieve = entries.retrieve()

    destroy = entries.destroy()
