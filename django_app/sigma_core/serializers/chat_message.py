from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

ChatMessage = load_ressource("ChatMessage")

@serializers.set
class ChatMessageSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = ChatMessage.model
        fields = '__all__'
