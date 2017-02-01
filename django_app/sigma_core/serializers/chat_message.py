from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

ChatMessage = load_ressource("ChatMessage")

class ChatMessageSerializerSet(SerializerSet):

    class ChatMessageSerializer(serializers.ModelSerializer):
        """
            Basic default serializer for a ChatMessage.
            Include all fields
        """
        class Meta:
            model = ChatMessage.model
            fields = '__all__'
