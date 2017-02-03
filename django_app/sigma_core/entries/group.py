from sigma_api import entries, response
from sigma_api.importer import load_ressource

Group = load_ressource("Group")

class GroupEntrySet(entries.EntrySet):
    
    list = entries.list(
        lambda user, data: Group.objects,
        Group.serializers.list
    )
    
    # members = entries.colist(
        # GroupMembers.objects
    # )
    
    retrieve = entries.retrieve(
        lambda user, data : Group.objects,
        Group.serializers.default
    )
    
    create = entries.create(
        Group.serializers.default
    )
    
    update_right = entries.update(
        Group.serializers.default,
        'update_right'
    )
    
    @entries.global_entry()
    def test(user, data):
        # print("Ser", Group.serializers)
        # print("Serlist", Group.serializers.list)
        # print("Serlistbases", Group.serializers.list.__bases__)
        # print("Isinst", issubclass(Group.serializers.list, Group.serializers))
        # print("")
        # print("Serfields", Group.serializers.fields)
        # print("Serlistfields", Group.serializers.list.fields)
        # print("")
        # print("Ser dict", Group.serializers.__dict__)
        # print("List dict", Group.serializers.list.__dict__)
        # print("")
        ser = Group.serializers.list()
        # print("Ser inst", ser)
        print("Ser dict", ser.__dict__)
        raise response.UnauthenticatedException