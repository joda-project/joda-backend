from django.contrib.auth.models import User
from rest_framework_json_api import serializers

from joda_core.models import Author, Content, Tag


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


class ContentSerializer(serializers.ModelSerializer):
    included_serializers = {
        'files': 'joda_core.serializers.FileSerializer'
    }

    content_type = serializers.CharField(
        source='get_content_type', read_only=True)
    # files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        # exclude = ('polymorphic_ctype',)
        fields = ('id', 'files', 'content_type')
