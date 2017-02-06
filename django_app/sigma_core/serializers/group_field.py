from sigma_api.importer import load_ressource
from sigma_api import serializers
import re

GroupField = load_ressource("GroupField")

@serializers.set
class GroupFieldSerializerSet(serializers.drf.ModelSerializer):
    """
        Basic default serializer for a Group field.
        Include all fields.
    """
    
    class Meta:
        model = GroupField.model
        read_only_fields = ('pk', 'group', 'type', )
        fields = ('pk', 'group', 'name', 'type', 'accept', 'protected', 'multiple_values_allowed')
    
    group = serializers.drf.PrimaryKeyRelatedField(read_only=True)
    
    #*********************************************************************************************#
    
    accept_field_regex = [
        re.compile(r'^((-?[0-9]+)?_(-?[0-9]+)?)?$'),
        None,
        None,
        re.compile(r'^(((@|\.)?(\w+.)*\w+ +)*((@|\.)?(\w+\.)*\w+))?$'),
    ]
    
    def validate(self, data):
        """ Validator that checks the structure of the 'accept' field depending on the field 'type' """
        type = data.get("type", getattr(self.instance, "type", None))
        accept = data.get("accept", getattr(self.instance, "accept", None))
        if type == None or accept == None:
            raise serializers.ValidationError("Missing required arguments 'type' or 'accept'")
            
        reg = GroupFieldSerializerSet.accept_field_regex[type]
        if reg == None or reg.match(accept):
            return data
        else:
            raise serializers.drf.ValidationError({'accept': "For this specific field type, the accepted expressions are invalid."})
            
            
    #*********************************************************************************************#