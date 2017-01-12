from django.contrib.auth.models import User
from rest_framework_json_api import serializers

from joda_core.models import Author, Content, File, Tag


class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(
        source='get_content_type', read_only=True)

    class Meta:
        model = Content
        exclude = ('polymorphic_ctype',)


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('name', 'md5', 'file_type', 'added',
                  'user', 'label', 'content_set')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
