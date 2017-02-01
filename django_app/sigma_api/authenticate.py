import oauth2_provider.models as oauth2models
from rest_framework import serializers

def authenticate(token):
    try:
        auth = oauth2models.AccessToken.objects.get(token=token)
        return auth
        
    except oauth2models.AccessToken.DoesNotExist:
        return None