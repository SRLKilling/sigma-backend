from rest_framework import serializers
from sigma_core.importer import load_ressource

Chat = load_ressource("Chat")


class ChatSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Chat.
        Include all fields
    """
    class Meta:
        model = Chat.model
        exclude = ('is_full_group_chat',)
