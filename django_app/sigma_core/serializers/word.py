from rest_framework import serializers

class WordSerializer(serializers.Serializer):

    word = serializers.CharField(required=True, allow_blank=True, max_length=100)
