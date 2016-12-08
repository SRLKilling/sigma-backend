from rest_framework import serializers

from sigma_core.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a User.
        Exclude useless fields : password, su, is_active
    """
    class Meta:
        model = User
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