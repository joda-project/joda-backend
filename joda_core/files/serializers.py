from rest_framework_json_api import serializers, relations

from joda_core.files.models import File


class FileProtectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        resource_name = 'files'
        fields = ('public',)


class FileSerializer(serializers.ModelSerializer):
    included_serializers = {
        'contents': 'joda_core.serializers.ContentSerializer'
    }
    contents = relations.ResourceRelatedField(
        source='content_set', many=True, read_only=True)

    def to_representation(self, instance):
        user = self.context['request'].user
        if not user.is_authenticated and not instance.public:
            f = FileProtectedSerializer(instance, context=self.context).to_representation(instance)
            f['content'] = []
            return f
        return super(FileSerializer, self).to_representation(instance)

    class Meta:
        model = File
        resource_name = 'files'
        fields = ('name', 'md5', 'size', 'file_type',
                  'added', 'public', 'label', 'contents')
