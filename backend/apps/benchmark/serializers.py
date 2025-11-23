from rest_framework import serializers
from .models import Bank, Product, Criterion, Source, Snapshot, FeatureValue, ParseLog


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name', 'website']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']


class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterion
        fields = ['id', 'name', 'description']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'description']


class FeatureValueSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    criterion_name = serializers.CharField(source='criterion.name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True, allow_null=True)

    class Meta:
        model = FeatureValue
        fields = [
            'bank',
            'bank_name',
            'criterion',
            'criterion_name',
            'value',
            'confidence',
            'source',
            'source_name',
            'source_url',
            'created_at',
        ]


class SnapshotSerializer(serializers.ModelSerializer):
    features = FeatureValueSerializer(many=True, read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Snapshot
        fields = [
            'id',
            'product',
            'product_name',
            'created_at',
            'features',
            'parsing_status',
            'note',
        ]


class ComparisonDataSerializer(serializers.Serializer):
    """Сериализер для API ответа /api/compare"""
    date = serializers.DateTimeField()
    sources = SourceSerializer(many=True)
    data = serializers.DictField()
    confidence = serializers.DictField(required=False, allow_empty=True)
    note = serializers.CharField(required=False, allow_blank=True)


class AIAnalysisResultSerializer(serializers.Serializer):
    """Сериализер для результатов AI анализа"""
    id = serializers.IntegerField(read_only=True)
    competitor = serializers.CharField()
    product = serializers.CharField()
    criterion = serializers.CharField()
    analysis_type = serializers.CharField()
    value = serializers.CharField(required=False, allow_null=True)
    source_url = serializers.URLField(required=False, allow_null=True)
    parsed_at = serializers.DateTimeField()
    analysis_at = serializers.DateTimeField(read_only=True)
    llm_model = serializers.CharField()
    llm_prompt_version = serializers.CharField()
    confidence_score = serializers.FloatField(required=False, allow_null=True)

