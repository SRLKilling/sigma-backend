from rest_framework import serializers
from sigma_core.importer import load_ressource

Comment = load_ressource("Comment")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment.model
        exclude = ()
