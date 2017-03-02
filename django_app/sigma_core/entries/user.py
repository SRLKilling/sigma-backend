from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")
UserConnection = load_ressource("UserConnection")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        serializer = User.serializers.list
    )

    retrieve = entries.retrieve(
        serializer = User.serializer.from_relation
    )
