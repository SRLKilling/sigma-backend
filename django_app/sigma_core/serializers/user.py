from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

User = load_ressource("User")

class UserSerializerSet(SerializerSet):

    class default(serializers.ModelSerializer):
        """
            Basic default serializer for a User.
            Exclude useless fields : password, su, is_active
        """
        class Meta:
            model = User.model
            exclude = ('password', 'is_superuser', 'is_staff')
            read_only_fields = ('is_active', 'photo', )
            extra_kwargs = {'password': {'write_only': True, 'required': False}}

        
        
    # class MinimalUserSerializer(serializers.ModelSerializer):
        # """
        # Serialize an User with minimal data.
        # """
        # class Meta:
            # model = User
            # fields = ('id', 'lastname', 'firstname', 'is_active')
            # read_only_fields = ('is_active', )