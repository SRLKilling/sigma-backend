from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        User.objects.user_can_see,
        User.serializers.list
    )

    retrieve = entries.retrieve()
