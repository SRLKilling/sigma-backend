from rest_framework import serializers

from sigma_core.models.user_connection import UserConnection


class UserConnectionSerializer(serializers.ModelSerializer):
    """
        Basic default serializer for a UserConnection.
        Include all fields
    """
    class Meta:
        model = UserConnection
        fields = '__all__'
