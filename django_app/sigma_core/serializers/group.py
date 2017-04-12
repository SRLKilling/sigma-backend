from sigma_api.importer import load_ressource
from sigma_api import serializers

Group = load_ressource("Group")
GroupField = load_ressource("GroupField")
GroupMember = load_ressource("GroupMember")

@serializers.set
class GroupSerializerSet(serializers.drf.ModelSerializer):

    number_of_members = serializers.drf.SerializerMethodField()
    score = serializers.drf.SerializerMethodField()

    class Meta:

        model = Group.model
        read_only_fields = ('pk', 'fields')
        fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility', 'fields','number_of_members', 'score')

    def get_number_of_members(self, obj):
        return GroupMember.objects.filter(group=obj).count()

    def get_score(self, user):
        return 1 #TODO : create a formula for the score

    fields = GroupField.serializers.default(many=True, read_only=True)

#*********************************************************************************************#

    @serializers.sub
    class list:
        class Meta:
            fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility','number_of_members', 'score')

    @serializers.sub
    class search:
        class Meta:
            fields = ('pk', 'name', 'number_of_members','score')
