from sigma_api import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Chat = load_ressource("Chat")
ChatMember = load_ressource("ChatMember")

@serializers.set
class ChatSerializerSet(serializers.drf.ModelSerializer):

    number_of_members = serializers.drf.SerializerMethodField()

    class Meta:

        model = Chat.model
        #exclude = ('is_full_group_chat',)

    def get_number_of_members(self, obj):
        return ChatMember.filter(chat=obj).count()

    @serializers.sub
    class list:
        class Meta:
            fields = None
            exclude = ('is_full_group_chat', 'group')
