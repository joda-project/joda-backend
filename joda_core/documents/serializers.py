from rest_framework_json_api import serializers

from joda_core.documents.models import Document


class DocumentAbstractSerializer(serializers.ModelSerializer):
    document_type = serializers.CharField(
        source='get_document_type', read_only=True)

    class Meta:
        model = Document


class DocumentSimpleSerializer(DocumentAbstractSerializer):

    class Meta(DocumentAbstractSerializer.Meta):
        fields = ('document_type', 'public', 'verified')


class DocumentSerializer(DocumentAbstractSerializer):
    included_serializers = {
        'files': 'joda_core.files.serializers.FileSerializer'
    }

    class Meta(DocumentAbstractSerializer.Meta):
        exclude = ('polymorphic_ctype', 'changed_by', 'changed_at')
