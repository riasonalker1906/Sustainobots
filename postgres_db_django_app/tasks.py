import parsagon
from celery.app import shared_task

from postgres_db_django_app.models import PublicationJournal, SearchTerm, Crop, Publication, SearchResults
from pub_scraping.pub_url_to_text import get_newspaper_data
from pub_scraping.scrape_links import auth_parsagon


@shared_task
def get_links(search_results_id):

    search_results = SearchResults.objects.get(id=search_results_id)

    auth_parsagon()
    journal = search_results.journal
    search_term = search_results.search_term
    crop = search_results.crop

    combined_search_term = f"{crop.name} AND {search_term.term}"
    data = parsagon.run(
        journal.scraper_id,
        variables={"search_term": combined_search_term},
        headless=True,
    )
    instances = []
    for pub in data:
        url = pub["link"]
        try:
            pub_instance = Publication.objects.create(title=pub["title"], url=url, journal=journal, crop=crop, search_term=search_term, data=None)
            instances.append(pub_instance)
            search_results.publications.add(pub_instance)
        except Exception as e:
            print(f"Error creating publication: {e}")


@shared_task
def get_publication_body(publication_id):
    publication = Publication.objects.get(id=publication_id)
    data = get_newspaper_data(publication.url)
    if not data:
        data = {"error": "No data found"}
    publication.data = data
    publication.save()


