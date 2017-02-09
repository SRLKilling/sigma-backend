from rest_framework import status
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import Sigma, load_ressource
from sigma_core.serializer.word import WordSerializer
from sigma_core.api import shortcuts

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")
Search = load_ressource("Search")
AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class SearchViewSet(SigmaViewSet):

    @entries.global_entry()
    def print_list(user, data):
        """
            REST list action. Used to list all groups a user can see.
        """

        word=shortcuts.get_validated_serializer(WordSerializer,data=data).validated_data.word

        group_qs = Group.objects.filter(name__contains = word)
        user_qs = User.objects.filter(name__contains = word)

        group_serializer = Group.serializer.list(group_qs,many=True)
        user_serializer = User.serializer.list(user_qs,many=True)
        search_serializer = Search.Serializer(user=user_serializer,group=group_serializer)

        return response.Response(response.Success_Retrieved, search_serializer.data)
