import httpx
import lxml.html
from newspaper import Article


def get_links_in_text(html, text):
    root = lxml.html.fromstring(html)
    links = root.findall(".//a[@href]")
    results = {}
    for link in links:
        link_text = link.xpath("normalize-space()")
        link_index = text.find(link_text)
        if link_text and link_index >= 0:
            results[link_index] = {"text": link_text, "url": link.get("href")}
    return results


def get_newspaper_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
    }
    try:
        r = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
    except httpx.RequestError:
        return None
    article = Article(url)
    try:
        article.download(input_html=r.text)
        article.parse()
    except:
        return None
    if (
        not article.title
        or not article.publish_date
        or not article.text
        or len(article.text) < 150
    ):
        return None
    article_links = get_links_in_text(r.text, article.text)
    return {
        "title": article.title,
        "authors": article.authors,
        "date_published": article.publish_date.isoformat(),
        "text": article.text,
        "link": str(r.url),
        "article_links": article_links,
    }
