from rest_framework import serializers

from sigma_core.models.chat import Chat


class ChatSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Chat.
        Include all fields
    """
    class Meta:
        model = Chat
        exclude = ('is_full_group_chat',)
