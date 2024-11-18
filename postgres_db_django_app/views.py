from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
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
from .serializers import (
    SearchTermSerializer,
    MetricsCategorySerializer,
    MetricSerializer,
    TechnicalStepSerializer,
    PublicationJournalSerializer,
    PublicationSerializer,
    CropSerializer,
    OrderedRankingSerializer,
)


class SearchTermViewSet(ReadOnlyModelViewSet):
    queryset = SearchTerm.objects.all()
    serializer_class = SearchTermSerializer


class MetricsCategoryViewSet(ReadOnlyModelViewSet):
    queryset = MetricsCategory.objects.all()
    serializer_class = MetricsCategorySerializer


class MetricViewSet(ReadOnlyModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class TechnicalStepViewSet(ReadOnlyModelViewSet):
    queryset = TechnicalStep.objects.all()
    serializer_class = TechnicalStepSerializer


class PublicationJournalViewSet(ReadOnlyModelViewSet):
    queryset = PublicationJournal.objects.all()
    serializer_class = PublicationJournalSerializer


class PublicationViewSet(ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class CropViewSet(ReadOnlyModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class OrderedRankingViewSet(ReadOnlyModelViewSet):
    queryset = OrderedRanking.objects.all()
    serializer_class = OrderedRankingSerializer
