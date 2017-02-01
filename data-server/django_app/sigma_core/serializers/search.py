from rest_framework import serializers
from sigma_core.importer import load_ressource

Search = load_ressource("Search")
Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
User = load_ressource("User")


class SearchSerializer(serializers.Serializer):
    """
        Basic default serializer for a Search.
    """
    user = User.serializer(many=True)
    group = Group.serializer(many=True)
