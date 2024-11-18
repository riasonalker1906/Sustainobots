from django.contrib import admin
from .models import (
    SearchTerm,
    MetricsCategory,
    Metric,
    TechnicalStep,
    PublicationJournal,
    Publication,
    Crop,
    OrderedRanking, SearchResults,
)


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("term", "notes", "technical_step", "metrics_category", "metrics_subcategory")
    search_fields = ("term", "notes")


@admin.register(MetricsCategory)
class MetricsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category__name")


@admin.register(TechnicalStep)
class TechnicalStepAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(PublicationJournal)
class PublicationJournalAdmin(admin.ModelAdmin):
    list_display = ("name", "scraper_id", "url", "has_popup")
    search_fields = ("name", "scraper_id", "url")
    list_filter = ("has_popup",)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "crop", "search_term", "summary")
    search_fields = ("title", "url", "summary", "crop__name", "search_term__term")
    list_filter = ("crop", "search_term")


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(OrderedRanking)
class OrderedRankingAdmin(admin.ModelAdmin):
    list_display = ("prompt", "batch_size")
    search_fields = ("prompt",)


@admin.register(SearchResults)
class SearchResultsAdmin(admin.ModelAdmin):
    list_display = ("search_term", "crop", "journal")
    search_fields = ("search_term__term", "crop__name", "publications__title")
    list_filter = ("crop", "search_term")