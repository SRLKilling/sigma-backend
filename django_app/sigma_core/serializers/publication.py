from sigma_api import serializers
from sigma_api.importer import load_ressource

Publication = load_ressource("Publication")
Like = load_ressource("Like")
Tag = load_ressource("Tag")
Comment = load_ressource("Comment")

@serializers.set
class PublicationSerializerSet(serializers.drf.ModelSerializer):

    number_tags = serializers.drf.SerializerMethodField()
    number_likes = serializers.drf.SerializerMethodField()
    number_comments = serializers.drf.SerializerMethodField()

    class Meta:
        model = Publication.model
        fields = "__all__"

    def get_number_tags(self, publication):
        return Tag.objects.on_publication(publication).count()

    def get_number_likes(self, publication):
        return Like.objects.on_publication(publication).count()

    def get_number_comments(self, publication):
        return Comment.objects.on_publication(publication).count()
