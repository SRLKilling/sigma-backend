from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

AcknowledgmentInvitation = load_ressource("AcknowledgmentInvitation")

class AcknowledgmentInvitationSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for an Invitation to acknowledge a group
            Include all fields
        """
        class Meta:
            model = AcknowledgmentInvitation.model
            fields = ('acknowledged', 'acknowledged_by', 'issued_by_invitee', 'date')
            required = ('acknowledged', 'acknowledged_by', 'issued_by_invitee')