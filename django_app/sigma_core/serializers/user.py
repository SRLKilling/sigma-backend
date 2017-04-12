from sigma_api import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

User = load_ressource("User")

@serializers.set
class UserSerializerSet(serializers.drf.ModelSerializer):

    score = serializers.drf.SerializerMethodField()
    fullname = serializers.drf.SerializerMethodField()

    class Meta:
        model = User.model
        fields = ('id', 'lastname', 'firstname', 'school', 'join_date')
        read_only_fields = ('is_active', 'photo', )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    @serializers.sub
    class list:
        class Meta:
            fields = ('id', 'lastname', 'firstname', 'school','score')


    @serializers.sub
    class stranger:
        class Meta:
            fields = ('id', 'lastname', 'firstname', 'school','email')

    def get_score(self, user):
        return 1 #TODO : create a formula for the score

    @staticmethod
    def from_relation(user2, *args, **kwargs):
        user = kwargs['context'].get('user')
        if User.objects.are_connected(user, user2):
            return User.serializers.default(user2, *args, **kwargs)
        else:
            return User.serializers.stranger(user2, *args, **kwargs)

    @serializers.sub
    class search:
        class Meta:
            fields =  ('id', 'fullname')

    def get_fullname(self, user):
        return user.firstname+" "+user.lastname
