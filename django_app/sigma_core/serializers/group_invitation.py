from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

GroupInvitation = load_ressource("GroupInvitation")

class GroupInvitationSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for an Invitation.
            Include all fields
        """
        class Meta:
            model = GroupInvitation.model
            fields = ('group', 'invitee', 'issued_by_invitee', 'date')
            required = ('group', 'invitee', 'issued_by_invitee')