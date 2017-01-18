from rest_framework_json_api import serializers

from joda_core.models import Author, User, Tag


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
        resource_name = "users"
        fields = ('id', 'username', 'first_name', 'last_name')
