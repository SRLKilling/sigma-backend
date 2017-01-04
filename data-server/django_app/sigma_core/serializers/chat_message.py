from rest_framework import serializers
from sigma_core.importer import load_ressource

ChatMessage = load_ressource("ChatMessage")


class ChatMessageSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a ChatMessage.
        Include all fields
    """
    class Meta:
        model = ChatMessage.model
        fields = '__all__'
