import feedparser
from datetime import datetime, timedelta

SOURCES = [
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/"},
    {"name": "Lenny's Newsletter", "url": "https://www.lennysnewsletter.com/feed"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage?points=100"},
    {"name": "Benedict Evans", "url": "https://www.ben-evans.com/benedictevans/rss.xml"},
    {"name": "Salesforce Ben", "url": "https://www.salesforceben.com/feed/"},
    {"name": "Kyle Poyar", "url": "https://kylepoyar.substack.com/feed"},
    {"name": "The Rundown AI", "url": "https://www.therundown.ai/feed"},
]

def fetch_recent_articles(days_back=7):
    cutoff = datetime.now() - timedelta(days=days_back)
    articles = []

    for source in SOURCES:
        print(f"Fetching: {source['name']}...")
        feed = feedparser.parse(source["url"])

        for entry in feed.entries[:10]:  # max 10 per source
            # parse published date
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])

            # skip if older than cutoff
            if published and published < cutoff:
                continue

            articles.append({
                "source": source["name"],
                "title": entry.get("title", "No title"),
                "url": entry.get("link", ""),
                "summary": entry.get("summary", "")[:500],  # trim long summaries
                "published": published.strftime("%Y-%m-%d") if published else "Unknown",
            })

    print(f"\nFetched {len(articles)} articles from the last {days_back} days")
    return articles