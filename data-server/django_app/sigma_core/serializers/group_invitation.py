from rest_framework import serializers
from sigma_core.importer import load_ressource

GroupInvitation = load_ressource("GroupInvitation")

class GroupInvitationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for an Invitation.
        Include all fields
    """
    class Meta:
        model = GroupInvitation.model
        fields = ('group', 'invitee', 'issued_by_invitee', 'date')
        required = ('group', 'invitee', 'issued_by_invitee')