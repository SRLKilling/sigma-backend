from rest_framework import serializers

from sigma_core.models.group_invitation import GroupInvitation

class GroupInvitationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for an Invitation.
        Include all fields
    """
    class Meta:
        model = GroupInvitation
        fields = ('group', 'invitee', 'issued_by_invitee', 'date')
        required = ('group', 'invitee', 'issued_by_invitee')