from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

ChatMember = load_ressource("ChatMember")

class ChatMemberSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a ChatMember.
            Include all fields
        """
        class Meta:
            model = ChatMember.model
            exclude = ('join_date', )
