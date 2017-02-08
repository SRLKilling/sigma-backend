from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

ChatMember = load_ressource("ChatMember")

@serializers.set
class ChatMemberSerializerSet(SerializerSet):

    class Meta:
        model = ChatMember.model
        #exclude = ('join_date', )
