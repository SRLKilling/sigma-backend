from sigma_api.importer import load_ressource
from sigma_api import shortcuts, entries, response
from sigma_core.serializers.word import WordSerializer
from django.db.models import Q

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")
Event = load_ressource("Event")
Search = load_ressource("Search")
AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class SearchEntrySet(entries.EntrySet):

    @entries.global_entry(method=["post"])
    def groups(user, data):
        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data["word"]
        group_qs = Search.model.groups(user, word)
        return shortcuts.list(user, data, group_qs, Group.serializer.search)

    @entries.global_entry(method=["post"])
    def users(user, data):
        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data["word"]
        user_qs = Search.model.users(user, word)
        return shortcuts.list(user, data, user_qs, User.serializer.search)

    @entries.global_entry(method=["post"])
    def events(user, data):
        word = shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data["word"]
        event_qs = Search.model.events(user, word)
        return shortcuts.list(user, data, event_qs, Event.serializer.search)
