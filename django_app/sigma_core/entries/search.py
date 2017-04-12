from sigma_api.importer import load_ressource
from sigma_api import shortcuts, entries, response
from sigma_core.serializers.word import WordSerializer
from django.db.models import Q

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")
Search = load_ressource("Search")
AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class SearchEntrySet(entries.EntrySet):

    @entries.global_entry(method=["post"])
    def groups(user, data):
        """
            REST list action.
        """

        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data["word"]

        group_qs = Group.objects.filter(name__contains = word)

        return shortcuts.list(user, data, group_qs, Group.serializer.search)

    @entries.global_entry(method=["post"])
    def users(user, data):
        """
            REST list action.
        """

        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data["word"]

        user_qs = User.objects.filter(Q(firstname__contains = word) | Q(lastname__contains = word))

        return shortcuts.list(user, data, user_qs, User.serializer.search)
