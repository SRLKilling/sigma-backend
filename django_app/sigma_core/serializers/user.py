from sigma_api import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

User = load_ressource("User")

@serializers.set
class UserSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = User.model
        exclude = ('password', 'is_superuser', 'is_staff')
        read_only_fields = ('is_active', 'photo', )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    @serializers.sub
    class list:
        class Meta:
            fields = ('lastname', 'firstname', 'school')


    @serializers.sub
    class stranger:
        class Meta:
            fields = ('lastname', 'firstname', 'school','email')




    # class MinimalUserSerializer(serializers.ModelSerializer):
        # """
        # Serialize an User with minimal data.
        # """
        # class Meta:
            # model = User
            # fields = ('id', 'lastname', 'firstname', 'is_active')
            # read_only_fields = ('is_active', )
