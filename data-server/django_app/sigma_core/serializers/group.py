from rest_framework import serializers

from sigma_core.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Group.
        Include all fields
    """
    class Meta:
        model = Group
        fields = ['pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility']
