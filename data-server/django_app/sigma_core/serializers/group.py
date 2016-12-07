from rest_framework import serializers

from sigma_core.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a Group.
        Include all fields
    """
    class Meta:
        model = Group
