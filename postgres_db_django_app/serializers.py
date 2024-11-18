from rest_framework import serializers
from .models import (
    SearchTerm,
    MetricsCategory,
    Metric,
    TechnicalStep,
    PublicationJournal,
    Publication,
    Crop,
    OrderedRanking,
)


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        fields = '__all__'


class MetricsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsCategory
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class TechnicalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalStep
        fields = '__all__'


class PublicationJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationJournal
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class OrderedRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedRanking
        fields = '__all__'
