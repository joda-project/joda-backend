from rest_framework_json_api import serializers

from joda_core.models import User
from joda_core.organization.models import Section, UserGroup


class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'readable_sections', 'writable_sections')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    user_groups = UserGroupSerializer(many=True, read_only=True)
    gravatar = serializers.CharField(
        source='generate_gravatar', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff',
                  'user_groups', 'locale', 'remote_avatar', 'gravatar')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'name')
