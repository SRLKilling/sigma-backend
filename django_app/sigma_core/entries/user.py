from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        User.objects.get_visible_users,
        User.serializers.list
    )

    retrieve = entries.retrieve()
