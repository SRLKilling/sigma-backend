from sigma_api import entries, response
from sigma_api.importer import load_ressource

UserConnection = load_ressource("UserConnection")

class UserConnectionEntrySet(entries.EntrySet):
    """
    this class works but there is nothing a user can directly do to modify
    this type of objects, it's completely handled in the code
    """
    pass
