from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Chat = load_ressource("Chat")

class ChatSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a Chat.
            Include all fields
        """
        class Meta:
            model = Chat.model
            exclude = ('is_full_group_chat',)
