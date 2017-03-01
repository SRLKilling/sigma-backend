from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")
UserConnection = load_ressource("UserConnection")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        User.objects,
        User.serializers.list
    )

    @entries.detailed_entry(methods=["post"])
    def retrieve(user, data, pk):
        u2 = User.objects.get(user=pk)

        if u2==None:
            return response.response(response.InvalidRequest)
        else:
            if UserConnection.objects.are_connected(user, u2):
                return shortcuts.retrieve(user, data, pk, User.objects.all, User.serializer.default)
            else:
                return shortcuts.retrieve(user, data, pk, User.objects.all, User.serializer.stranger)
