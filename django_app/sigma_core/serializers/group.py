from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Group = load_ressource("Group")
GroupField = load_ressource("GroupField")

class GroupSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a Group.
            Include all fields
        """
        class Meta:
            model = Group.model
            fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility', 'fields')
        
        fields = GroupField.serializers.default(many=True, read_only=True)
        
        
    class list(serializers.ModelSerializer):
        """
            Basic default serializer for a Group.
            Include all fields
        """
        class Meta:
            model = Group.model
            fields = ('pk', 'name', 'description', 'fields')
        
        fields = GroupField.serializers.default(many=True, read_only=True)