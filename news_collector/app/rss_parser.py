import feedparser
import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    "http://feeds.venturebeat.com/VentureBeat",
    "https://www.producthunt.com/feed"
]

def parse_rss():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            article = {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "media": []
            }
            # Извлечение полного текста и медиа
            try:
                response = requests.get(article["link"], timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")
                article["full_text"] = soup.get_text(strip=True)
                images = [img["src"] for img in soup.find_all("img") if "src" in img.attrs]
                article["media"].extend(images)
            except Exception as e:
                print(f"Ошибка при загрузке {article['link']}: {e}")
            articles.append(article)
    return articles
