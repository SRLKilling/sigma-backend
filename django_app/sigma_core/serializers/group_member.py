from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

GroupMember = load_ressource("GroupMember")

class GroupMemberSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a GroupMember.
            Include all fields
        """
        class Meta:
            model = GroupMember.model
            fields = '__all__'
        
        
    class rights(serializers.ModelSerializer):
        """
            Serializer for a GroupMember including only permissions fields.
        """
        class Meta:
            model = GroupMember.model
            fields = ('is_administrator', 'is_super_administrator', 'has_invite_right', 'has_contact_right', 'has_publish_right', 'has_kick_right')
