from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Chat = load_ressource("Chat")

@serializers.set
class ChatSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Chat.model
        exclude = ('is_full_group_chat',)


    @serializers.sub
    class list:
        class Meta:
            fields = None
            #exclude = ('fields', )
