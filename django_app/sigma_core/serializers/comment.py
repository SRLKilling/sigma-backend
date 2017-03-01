from rest_framework import serializers
from sigma_api.importer import load_ressource
from sigma_api.serializers import SerializerSet

Comment = load_ressource("Comment")

class CommentSerializerSet(SerializerSet):

    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment.model
            exclude = ()
