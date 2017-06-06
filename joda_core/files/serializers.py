from rest_framework_json_api import serializers, relations

from joda_core.files.models import File


class FileProtectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('public',)


class FileSerializer(serializers.ModelSerializer):
    included_serializers = {
        'documents': 'joda_core.documents.serializers.DocumentSimpleSerializer'
    }
    name = serializers.CharField(source='__str__', read_only=True)
    documents = relations.ResourceRelatedField(
        source='document_set', many=True, read_only=True)

    def to_representation(self, instance):
        user = self.context['request'].user
        if not user.is_authenticated and not instance.public:
            f = FileProtectedSerializer(instance, context=self.context).to_representation(instance)
            f['created_by'] = []
            f['sections'] = []
            f['documents'] = []
            return f
        return super(FileSerializer, self).to_representation(instance)

    class Meta:
        model = File
        exclude = ('changed_at', 'changed_by')
