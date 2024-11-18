from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SearchTermViewSet,
    MetricsCategoryViewSet,
    MetricViewSet,
    TechnicalStepViewSet,
    PublicationJournalViewSet,
    PublicationViewSet,
    CropViewSet,
    OrderedRankingViewSet,
)

router = DefaultRouter()
router.register(r'search-terms', SearchTermViewSet)
router.register(r'metrics-categories', MetricsCategoryViewSet)
router.register(r'metrics', MetricViewSet)
router.register(r'technical-steps', TechnicalStepViewSet)
router.register(r'publication-journals', PublicationJournalViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'crops', CropViewSet)
router.register(r'ordered-rankings', OrderedRankingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
