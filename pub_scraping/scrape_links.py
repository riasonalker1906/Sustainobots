import json
import os
from pathlib import Path

from django.conf import settings
from django.forms import model_to_dict

from postgres_db_django_utils import manage_command

import parsagon


def auth_parsagon():
    # Copy parsagon_profile.json to the home directory
    home = str(Path.home())
    settings_file = ".parsagon_profile"
    settings_path = os.path.join(home, settings_file)
    if not os.path.exists(settings_path):
        with open(settings_path, "w") as f:
            f.write(json.dumps({"api_key": settings.PARSAGON_API_KEY}))


@manage_command
def create_scrapers():
    auth_parsagon()

    from postgres_db_django_app.models import PublicationJournal, Crop

    # Connects to Parsagon server to create scrapers
    for source in PublicationJournal.objects.all():
        source = model_to_dict(source)
        url = source["url"]
        if source.get("has_popup"):
            popup_remove = " Click the accept all cookies button."
        else:
            popup_remove = ""
        parsagon.create(
            f'Go to {url}.{popup_remove} Type {{search_term:bioreactor}} in the search bar.  Press enter.  Then wait for the resulting page to load.  Scroll to the bottom of the page.  Scrape articles from the page in the format: {{ "title": "str", "link": "link" }}'
        )


@manage_command
def scrape_links():
    from postgres_db_django_app.models import Publication
    from postgres_db_django_app.models import Crop
    from postgres_db_django_app.models import (
        SearchTerm,
        PublicationJournal,
        SearchResults,
    )

    # Requires Parsagon server and create_scrapers called

    for crop in Crop.objects.all():
        for search_term in SearchTerm.objects.all():
            for source in PublicationJournal.objects.all():
                SearchResults.objects.filter(
                    crop=crop,
                    search_term=search_term,
                    journal=source,
                ).delete()
                try:
                    SearchResults.objects.create(
                        crop=crop,
                        search_term=search_term,
                        journal=source,
                    )
                except Exception as e:
                    print(f"Error creating SearchResults: {e}")


if __name__ == "__main__":
    # create_scrapers()
    scrape_links()
