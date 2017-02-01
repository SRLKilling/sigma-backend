from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet
import re

GroupField = load_ressource("GroupField")

class GroupFieldSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a Group field.
            Include all fields.
        """
        
        class Meta:
            model = GroupField.model
            read_only_fields = ('group', )
            fields = ('group', 'name', 'type', 'accept', 'protected', 'multiple_values_allowed')
        

        #*********************************************************************************************#
        #**                                     Validators                                          **#
        #*********************************************************************************************#
        
        # "Acceptable values" field validator
        accept_field_regex = [
            re.compile(r'^((-?[0-9]+)?_(-?[0-9]+)?)?$'),
            None,
            None,
            re.compile(r'^(((@|\.)?(\w+.)*\w+ +)*((@|\.)?(\w+\.)*\w+))?$'),
        ]
        
        def validate(self, data):
            """
                Validator that checks the structure of the 'accept' field depending on the field 'type'
            """
            if GroupFieldSerializer.accept_field_regex[data['type']] == None or ('accept' in data and GroupFieldSerializer.accept_field_regex[data['type']].match(data['accept'])):
                return data
                
            else:
                raise serializers.ValidationError("Le format des valeurs acceptables n'est pas valable.")