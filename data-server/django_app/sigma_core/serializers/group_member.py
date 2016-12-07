from rest_framework import serializers

from sigma_core.models.group_member import GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a GroupMember.
        Include all fields
    """
    class Meta:
        model = GroupMember
        fields = '__all__'
    
    
class GroupMemberRightSerializer(serializers.ModelSerializer):
    """
        Serializer for a GroupMember including only permissions fields.
    """
    class Meta:
        model = GroupMember
        fields = ('is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right')
