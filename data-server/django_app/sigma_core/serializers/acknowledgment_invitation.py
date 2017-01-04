from rest_framework import serializers
from sigma_core.importer import load_ressource

AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")


class AcknowledgmentInvitationSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for an Invitation to acknowledge a group
        Include all fields
    """
    class Meta:
        model = AcknowledgmentInvitation.model
        fields = ('acknowledged', 'acknowledged_by', 'issued_by_invitee', 'date')
        required = ('acknowledged', 'acknowledged_by', 'issued_by_invitee')