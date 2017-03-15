from sigma_api.importer import load_ressource
from sigma_api import shortcuts, entries
from sigma_core.serializers.word import WordSerializer

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")
Search = load_ressource("Search")
AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class SearchEntrySet(entries.EntrySet):

    @entries.global_entry(methods=["post"])
    def print_list(user, data):
        """
            REST list action.
        """

        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data.word

        group_qs = Group.objects.filter(name__contains = word)
        user_qs = User.objects.filter(name__contains = word)

        group_serializer = Group.serializer.list(group_qs,many=True)
        user_serializer = User.serializer.list(user_qs,many=True)
        search_serializer = Search.Serializer(user=user_serializer,group=group_serializer)

        return response.Response(response.Success_Retrieved, search_serializer.data)

    @entries.global_entry(bind_set=True, methods=["post"])
    def create(self, user, data):

        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data.word

        group_qs = Group.objects.filter(name__contains = word)
        user_qs = User.objects.filter(name__contains = word)

        group_serializer = Group.serializer.list(group_qs,many=True)
        user_serializer = User.serializer.list(user_qs,many=True)
        search_serializer = Search.Serializer(user=user_serializer,group=group_serializer)

        return response.Response(response.Success_Retrieved, search_serializer.data)
