from sigma_api.importer import load_ressource
from sigma_api import serializers

GroupMember = load_ressource("GroupMember")
GroupFieldValue = load_ressource("GroupFieldValue")

@serializers.set
class GroupMemberSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = GroupMember.model
        fields = ('pk', 'user', 'group', 'created', 'hidden',
                'is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right', 'field_values')

    group = serializers.drf.PrimaryKeyRelatedField(read_only=True)
    user = serializers.drf.PrimaryKeyRelatedField(read_only=True)

    field_values = GroupFieldValue.serializers.default(many=True, read_only=True)

#*********************************************************************************************#

    @serializers.sub
    class list:
        class Meta:
            fields = ('pk', 'user', 'group', 'created', 'hidden',
                    'is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right')

    @serializers.sub
    class retrieve:
        class Meta:
            read_only_fields = ('pk', 'field_values')
            fields = ('pk', 'user', 'group', 'created', 'hidden',
                    'is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right', 'field_values')



    @serializers.sub
    class update:
        class Meta:
            fields = ('pk',
                    'is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right')
