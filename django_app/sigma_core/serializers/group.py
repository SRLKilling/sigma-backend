from sigma_api.importer import load_ressource
from sigma_api import serializers

Group = load_ressource("Group")
GroupField = load_ressource("GroupField")

@serializers.set
class GroupSerializerSet(serializers.drf.ModelSerializer):
    class Meta:
        model = Group.model
        read_only_fields = ('pk', 'fields')
        fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility', 'fields')
    
    fields = GroupField.serializers.default(many=True, read_only=True)
    
#*********************************************************************************************#
        
    @serializers.sub
    class list:
        class Meta:
            fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility')