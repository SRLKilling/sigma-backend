from sigma_api import serializers
from sigma_api.importer import load_ressource

Comment = load_ressource("Comment")

@serializers.set
class CommentSerializerSet(serializers.drf.ModelSerializer):

    class Meta:
        model = Comment.model
        exclude = ()
