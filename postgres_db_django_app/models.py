from django.db import models


class SearchTerm(models.Model):
    term = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, null=True, blank=True)

    technical_step = models.ForeignKey("TechnicalStep", on_delete=models.CASCADE, related_name="search_terms", null=True, blank=True)
    metrics_category = models.ForeignKey("MetricsCategory", on_delete=models.SET_NULL, related_name="search_terms", null=True, blank=True)
    metrics_subcategory = models.CharField(max_length=255, null=True, blank=True)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.technical_step:
            self.metrics_category = MetricsCategory.objects.get(name="Technical")
        super().save(*args, force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"SearchTerm: {self.term}"


class MetricsCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"MetricsCategory: {self.name}"


class Metric(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey("MetricsCategory", on_delete=models.CASCADE, related_name="metrics")
    crop = models.ForeignKey("Crop", on_delete=models.CASCADE, related_name="metrics", null=True)
    value = models.FloatField(null=True, blank=True)
    units = models.CharField(max_length=255, null=True, blank=True)
    publication = models.ForeignKey("Publication", on_delete=models.SET_NULL, related_name="metrics", null=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Metric: {self.name} (Category: {self.category.name})"


class TechnicalStep(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"TechnicalStep: {self.name}"


class PublicationJournal(models.Model):
    name = models.CharField(max_length=255)
    scraper_id = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    has_popup = models.BooleanField(default=False)

    def __str__(self):
        return f"Journal: {self.name}"


class SearchResults(models.Model):
    search_term = models.ForeignKey("SearchTerm", on_delete=models.CASCADE, related_name="search_results")
    crop = models.ForeignKey("Crop", on_delete=models.CASCADE, related_name="search_results")
    journal = models.ForeignKey("PublicationJournal", on_delete=models.CASCADE, related_name="search_results")
    publications = models.ManyToManyField("Publication", related_name="search_results", blank=True)

    class Meta:
        unique_together = ("search_term", "crop", "journal")

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(*args, force_insert, force_update, using, update_fields)
        from postgres_db_django_app.tasks import get_links
        get_links.delay(self.id)

    def __str__(self):
        return f"SearchResults: {self.search_term}"


class Publication(models.Model):
    title = models.CharField(max_length=512)
    url = models.CharField(max_length=255, unique=True)
    data = models.JSONField(null=True, blank=True)
    crop = models.ForeignKey("Crop", on_delete=models.CASCADE, related_name="publications", null=True)
    search_term = models.ForeignKey("SearchTerm", on_delete=models.CASCADE, related_name="publications", null=True)
    summary = models.TextField(null=True, blank=True)
    journal = models.ForeignKey("PublicationJournal", on_delete=models.CASCADE, related_name="publications", null=True)

    def __str__(self):
        return f"Publication: {self.title}"

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(*args, force_insert, force_update, using, update_fields)
        from postgres_db_django_app.tasks import get_publication_body
        if not self.data:
            get_publication_body.delay(self.id)


class Crop(models.Model):
    name = models.CharField(max_length=255, unique=True)
    emissions = models.FloatField(null=True, blank=True)
    emission_data = models.JSONField(null=True, blank=True)
    mentioned_in_world_bank = models.BooleanField(default=False)

    def __str__(self):
        return f"Crop: {self.name}"


class OrderedRanking(models.Model):
    prompt = models.TextField()
    batch_size = models.IntegerField(default=5)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.prompt = self.prompt.strip()
        super().save(*args, force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"OrderedRanking: {self.prompt[:50]}..."  # Limit display length

