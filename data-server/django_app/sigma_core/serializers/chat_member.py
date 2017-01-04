from rest_framework import serializers
from sigma_core.importer import load_ressource

ChatMember = load_ressource("ChatMember")


class ChatMemberSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a ChatMember.
        Include all fields
    """
    class Meta:
        model = ChatMember.model
        exclude = ('join_date', )
