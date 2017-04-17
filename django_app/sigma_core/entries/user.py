from sigma_api import entries, response
from sigma_api.importer import load_ressource

User = load_ressource("User")
UserConnection = load_ressource("UserConnection")
Publication = load_ressource("Publication")
Event = load_ressource("Event")
Participation = load_ressource("Participation")

class UserEntrySet(entries.EntrySet):

    list = entries.list(
        serializer = User.serializers.list
    )

    visible_users = entries.list(
        queryset = User.objects.get_visible_users,
        serializer = User.serializers.list
    )

    retrieve = entries.retrieve(
        serializer = User.serializer.from_relation
    )

    publications = entries.sub_list(
        sub_queryset = lambda u1, u2: Publication.objects.created_by(u1),
        serializer = Publication.serializer
    )

    events_created = entries.sub_list(
        sub_queryset = lambda u1, u2: Event.objects.created_by(u1),
        serializer = Event.serializer
    )

    interesting_events = entries.sub_list(
        sub_queryset = lambda u1, u2: Participation.objects.for_user(u1).interested(),
        serializer = Participation.serializer
    )

    invitations = entries.sub_list(
        sub_queryset = lambda u1, u2: Participation.objects.for_user(u1).invited(),
        serializer = Participation.serializer
    )
