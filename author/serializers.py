from rest_framework import serializers
from .models import Author
from urllib.parse import urlparse

from rest_framework import serializers
from urllib.parse import urlparse
from .models import Author

class AuthorSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, default="author")
    id = serializers.SerializerMethodField()  # 使用 SerializerMethodField 来自定义 id 的输出
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100)
    github = serializers.URLField(allow_null=True, required=False)
    profileImage = serializers.URLField(allow_null=True, required=False)
    page = serializers.URLField(allow_null=True, required=False)

    def get_id(self, obj):
        """
        返回 fqid 作为 id 的值
        """
        return obj.fqid  # 返回数据库中存储的 fqid 值

    def validate_id(self, value):
        """
        验证 id 的 URL，确保其格式符合要求
        """
        parsed_url = urlparse(value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise serializers.ValidationError("无效的 URL 格式")
        
        return value

    def create(self, validated_data):
        """
        创建并返回一个新的 Author 实例，基于验证后的数据。
        """
        validated_data['fqid'] = validated_data.pop('id')  # 将请求中的 id 映射到 fqid
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新并返回一个已存在的 Author 实例，基于验证后的数据。
        如果尝试修改 id 或 host，则返回错误。
        """
        # 验证 id 是否一致
        if 'id' in validated_data and validated_data['id'] != instance.fqid:
            raise serializers.ValidationError("不能修改 id 字段。")

        # 验证 host 是否一致
        if 'host' in validated_data and validated_data['host'] != instance.host:
            raise serializers.ValidationError("不能修改 host 字段。")

        # 更新其他可修改字段
        instance.type = validated_data.get('type', instance.type)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.page = validated_data.get('page', instance.page)
        instance.save()

        return instance
    
class FollowerSerializer(serializers.Serializer):
    type = serializers.CharField(default="author")
    id = serializers.URLField()  # 使用 fqid
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100)
    github = serializers.URLField(allow_null=True, required=False)
    profileImage = serializers.URLField(allow_null=True, required=False)
    page = serializers.URLField(allow_null=True, required=False)