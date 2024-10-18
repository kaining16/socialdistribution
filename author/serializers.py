from rest_framework import serializers
from .models import Author
from urllib.parse import urlparse

from rest_framework import serializers
from urllib.parse import urlparse
from .models import Author

class AuthorSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, default="author")
    id = serializers.SerializerMethodField()  
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100, allow_null=True, required=False)
    github = serializers.URLField(allow_null=True, required=False)
    profileImage = serializers.URLField(allow_null=True, required=False)
    page = serializers.URLField(allow_null=True, required=False)

    def get_id(self, obj):
        
        return obj.fqid  

    def validate_id(self, value):
        
        parsed_url = urlparse(value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise serializers.ValidationError("无效的 URL 格式")
        
        return value

    def create(self, validated_data):
        
        validated_data['fqid'] = validated_data.pop('id')  
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        
        if 'id' in validated_data and validated_data['id'] != instance.fqid:
            raise serializers.ValidationError("不能修改 id 字段。")

        
        if 'host' in validated_data and validated_data['host'] != instance.host:
            raise serializers.ValidationError("不能修改 host 字段。")

        
        instance.type = validated_data.get('type', instance.type)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.page = validated_data.get('page', instance.page)
        instance.save()

        return instance
    
class FollowerSerializer(serializers.Serializer):
    type = serializers.CharField(default="author")
    id = serializers.URLField()  
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100)
    github = serializers.URLField(allow_null=True, required=False)
    profileImage = serializers.URLField(allow_null=True, required=False)
    page = serializers.URLField(allow_null=True, required=False)


from rest_framework import serializers
from .models import FollowRequest, Author
from .serializers import AuthorSerializer

class FollowRequestSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, default="follow")
    summary = serializers.CharField(max_length=255)

    
    actor = AuthorSerializer()
    object = AuthorSerializer()

    def create(self, validated_data):
        
        actor_data = validated_data.pop('actor')
        object_data = validated_data.pop('object')

        
        actor, _ = Author.objects.get_or_create(
            fqid=actor_data['id'],
            defaults={
                'displayName': actor_data['displayName'],
                'host': actor_data['host'],
                'github': actor_data.get('github'),
                'profileImage': actor_data.get('profileImage'),
                'page': actor_data.get('page')
            }
        )

       
        target, _ = Author.objects.get_or_create(
            fqid=object_data['id'],
            defaults={
                'displayName': object_data['displayName'],
                'host': object_data['host'],
                'github': object_data.get('github'),
                'profileImage': object_data.get('profileImage'),
                'page': object_data.get('page')
            }
        )

        
        follow_request = FollowRequest.objects.create(
            request_type=validated_data.get('type', 'follow'),
            summary=validated_data['summary'],
            actor=actor,
            object=target,
        )
        return follow_request