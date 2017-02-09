from rest_framework_json_api import serializers

from joda_core.models import User
from joda_core.organization.models import Section, UserGroup


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff',
                  'user_groups', 'remote_avatar')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'name')


class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'readable_sections', 'writable_sections')
