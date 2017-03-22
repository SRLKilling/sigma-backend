from sigma_api import serializers
from sigma_api.importer import load_ressource

Search = load_ressource("Search")
Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")

@serializers.set
class SearchSerializerSet(serializers.drf.Serializer):
    """
        Basic default serializer for a Search
        IT ISN'T USED
    """
    user = User.serializer.list(many=True)
    group = Group.serializer.list(many=True)

    class Meta:
        model = Search.model
        fields = "__all__"
