from rest_framework import serializers

from sigma_core.models.acknowledgment_invitation import AcknowledgmentInvitation

class AcknowledgmentInvitationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for an Invitation to acknowledge a group
        Include all fields
    """
    class Meta:
        model = AcknowledgmentInvitation
        fields = ('acknowledged', 'acknowledged_by', 'issued_by_invitee', 'date')
        required = ('acknowledged', 'acknowledged_by', 'issued_by_invitee')