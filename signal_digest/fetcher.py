import feedparser
import os
import json
from datetime import datetime, timedelta

SOURCES = [
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/"},
    {"name": "Lenny's Newsletter", "url": "https://www.lennysnewsletter.com/feed"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage?points=100"},
    {"name": "Benedict Evans", "url": "https://www.ben-evans.com/benedictevans/rss.xml"},
    {"name": "Salesforce Ben", "url": "https://www.salesforceben.com/feed/"},
    {"name": "Kyle Poyar", "url": "https://kylepoyar.substack.com/feed"},
    {"name": "The Rundown AI", "url": "https://www.therundown.ai/feed"},
    {"name": "LangChain Blog", "url": "https://blog.langchain.dev/rss/"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "Andrew Chen", "url": "https://andrewchen.com/feed/"},
    {"name": "OpenView Partners", "url": "https://openviewpartners.com/feed/"},
    {"name": "GitHub Changelog", "url": "https://github.blog/changelog/feed/"},
]

CACHE_FILE = "cache.json"

def load_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return set(json.load(f).get("urls", []))
    except Exception:
        pass
    return set()

def save_cache(urls):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"urls": list(urls), "last_updated": datetime.now().strftime("%Y-%m-%d")}, f, indent=2)
    except Exception as e:
        print(f"  WARNING: Cache save error: {e}")

def fetch_recent_articles(days_back=7):
    cutoff = datetime.now() - timedelta(days=days_back)
    seen_urls = load_cache()
    articles = []
    failed_sources = []

    for source in SOURCES:
        try:
            print(f"Fetching: {source['name']}...")
            feed = feedparser.parse(source["url"])

            if feed.bozo and not feed.entries:
                print(f"  WARNING: {source['name']} feed error: {feed.bozo_exception}")
                failed_sources.append(source["name"])
                continue

            for entry in feed.entries[:10]:  # max 10 per source
                # parse published date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])

                # skip if older than cutoff
                if published and published < cutoff:
                    continue

                url = entry.get("link", "")

                # skip if already seen in a previous run
                if url in seen_urls:
                    continue

                articles.append({
                    "source": source["name"],
                    "title": entry.get("title", "No title"),
                    "url": url,
                    "summary": entry.get("summary", "")[:500],  # trim long summaries
                    "published": published.strftime("%Y-%m-%d") if published else "Unknown",
                })

        except Exception as e:
            print(f"  ERROR fetching {source['name']}: {e}")
            failed_sources.append(source["name"])
            continue

    if failed_sources:
        print(f"\nFailed sources ({len(failed_sources)}): {', '.join(failed_sources)}")

    save_cache(seen_urls | {a["url"] for a in articles})

    print(f"\nFetched {len(articles)} new articles from the last {days_back} days")
    return articles