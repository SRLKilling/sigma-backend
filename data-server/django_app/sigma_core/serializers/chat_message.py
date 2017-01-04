from rest_framework import serializers

from sigma_core.models.chat_message import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a ChatMessage.
        Include all fields
    """
    class Meta:
        model = ChatMessage
        fields = '__all__'
