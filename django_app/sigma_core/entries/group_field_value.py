from sigma_api import entries, response, shortcuts
from sigma_api.importer import load_ressource

GroupField = load_ressource("GroupField")
GroupFieldValue = load_ressource("GroupFieldValue")

class GroupFieldValueEntrySet(entries.EntrySet):
    
    @entries.global_entry(methods=["post"])
    def create(user, data):
        instance = shortcuts.get_deserialized_instance(GroupFieldValue.serializer, data=data)
        field = instance.field
        
        check_permission(user, instance, "create")
        if not field.multiple_values_allowed and GroupFieldValue.objects.filter(field=field).exists():
            raise response.InvalidRequestException("A value for this field already exists")
            
        instance.save()
        return response.Response(response.Success_Created, GroupFieldValue.serializer(instance).data)
        
        
    retrieve = entries.retrieve()
    
    update = entries.update()
    
    destroy = entries.destroy()