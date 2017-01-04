from rest_framework import serializers

from sigma_core.models.chat_member import ChatMember


class ChatMemberSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a ChatMember.
        Include all fields
    """
    class Meta:
        model = ChatMember
        exclude = ('join_date',)
