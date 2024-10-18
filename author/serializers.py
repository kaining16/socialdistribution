from rest_framework import serializers
from .models import Author
from urllib.parse import urlparse

from rest_framework import serializers
from urllib.parse import urlparse
from .models import Author

from rest_framework import serializers
from urllib.parse import urlparse
from .models import Author

class AuthorSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, default="author")
    #id accept id but show fqid when response
    id = serializers.SerializerMethodField()
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100, allow_null=True, required=False)
    github = serializers.URLField(allow_null=True, required=False)
    profileImage = serializers.URLField(allow_null=True, required=False)
    page = serializers.URLField(allow_null=True, required=False)

    def get_id(self, obj):
        #show fqid as id
        return obj.fqid 
    
    def update(self, instance, validated_data):
        #update the author, except id and host
        instance.type = validated_data.get('type', instance.type)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.page = validated_data.get('page', instance.page)
        instance.save()
        return instance

