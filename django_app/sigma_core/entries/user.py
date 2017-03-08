from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")
UserConnection = load_ressource("UserConnection")
Publication = load_ressource("Publication")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        serializer = User.serializers.list
    )

    retrieve = entries.retrieve(
        serializer = User.serializer.from_relation
    )

    publications = entries.sub_list(
        sub_queryset = lambda u1, u2: Publication.objects.created_by(u2),
        serializer = Publication.serializer
    )
