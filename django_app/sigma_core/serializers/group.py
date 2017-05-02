from sigma_api.importer import load_ressource
from sigma_api import serializers

Group = load_ressource("Group")
GroupField = load_ressource("GroupField")
GroupMember = load_ressource("GroupMember")

@serializers.set
class GroupSerializerSet(serializers.drf.ModelSerializer):

    number_of_members = serializers.drf.SerializerMethodField()
    score = serializers.drf.SerializerMethodField()
    status = serializers.drf.SerializerMethodField()

    class Meta:
        model = Group.model
        read_only_fields = ('pk', 'fields')
        fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility', 'fields','number_of_members', 'score','status')

    def get_number_of_members(self, obj):
        return GroupMember.objects.filter(group=obj).count()

    def get_score(self, obj):
        print(obj)
        print(self.context["user"])
        return max(1,GroupMember.objects.get(group=obj,user=self.context["user"]).average_clicks_last_month//10)

        #return max(1,GroupMember.objects.filter(group=group, user=self).count())


    def get_status(self, group):
        return "group"

    fields = GroupField.serializers.default(many=True, read_only=True)

#*********************************************************************************************#

    @serializers.sub
    class list:
        class Meta:
            fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility','number_of_members', 'score')

    @serializers.sub
    class search:
        class Meta:
            fields = ('id', 'name','score', 'status','number_of_members')

    @serializers.sub
    class update:
        class Meta:
            fields = ('id', 'description', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility')
