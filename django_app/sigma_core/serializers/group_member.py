from sigma_api.importer import load_ressource
from sigma_api import serializers

GroupMember = load_ressource("GroupMember")

@serializers.set
class GroupMemberSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = GroupMember.model
        fields = '__all__'

    group = serializers.drf.PrimaryKeyRelatedField(read_only=True)


#*********************************************************************************************#

    @serializers.sub
    class rights:
        """ Serializer for a GroupMember including only permissions fields. """
        class Meta:
            fields = ('is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right')
