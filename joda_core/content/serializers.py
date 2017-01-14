from rest_framework_json_api import serializers

from joda_core.content.models import Content


class ContentSimpleSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(
        source='get_content_type', read_only=True)

    class Meta:
        model = Content
        resource_name = 'contents'
        fields = ('content_type', 'public', 'verified')


class ContentSerializer(serializers.ModelSerializer):
    included_serializers = {
        'files': 'joda_core.files.serializers.FileSerializer'
    }

    content_type = serializers.CharField(
        source='get_content_type', read_only=True)

    class Meta:
        model = Content
        resource_name = "contents"
        exclude = ('polymorphic_ctype', 'user')
