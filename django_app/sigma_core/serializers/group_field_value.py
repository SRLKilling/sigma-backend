from sigma_api.importer import load_ressource
from sigma_api import serializers
import re

GroupFieldValue = load_ressource("GroupFieldValue")
GroupField = load_ressource("GroupField")

@serializers.set
class GroupFieldValueSerializerSet(serializers.drf.ModelSerializer):
    class Meta:
        model = GroupFieldValue.model
        read_only_fields = ('pk', 'membership', 'field')
        fields = ('pk', 'membership', 'field', 'value')

    membership = serializers.drf.PrimaryKeyRelatedField(read_only=True)


    #*********************************************************************************************#

    number_re = re.compile(r'^[+-]?[0-9]+$')
    def is_number_valid(self, accept, value):
        if accept == '' or (not GroupFieldValueSerializer.number_re.match(value)):
            return True

        value = int(value)
        a,b = accept.split('_')
        if not a == '':
            if not b == '':
                a, b = int(a), int(b)
                a, b = min(a,b), max(a,b)
                return a <= value and value <= b
            else:
                return int(a) <= value
        else:
            if not b == '':
                return value <= int(b)
            else:
                return True

    def is_string_valid(self, accept, value):
        return True

    def is_choice_valid(self, accept, value):
        if accept == '':
            return False
        choices = accept.split(';')
        return value in choices

    def is_email_valid(self, accept, value):
        if accept != '':
            suffixes = accept.split()
            return value.endswith(tuple(suffixes))
        return True

    def validate(self, data):
        group_field = data['field']
        mship = data['membership']

        # First, check that the membership group correspond to the field group
        if group_field.group != mship.group:
            raise serializers.ValidationError("Condition (field.group == membership.group) is not verified.")

        # Then, check that the content is valid
        validate_methods = [
            self.is_number_valid,
            self.is_string_valid,
            self.is_choice_valid,
            self.is_email_valid
        ]
        if validate_methods[group_field.type](group_field.accept, data['value']):
            return data
        else:
            raise serializers.ValidationError('Les données entrées sont invalides')

    #*********************************************************************************************#
