from sigma_api import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

ChatMember = load_ressource("ChatMember")

@serializers.set
class ChatMemberSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = ChatMember.model
        fields = '__all__'
        #exclude = ('join_date', )
