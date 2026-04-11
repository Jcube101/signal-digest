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
    {"name": "TLDR AI", "url": "https://tldr.tech/api/rss/ai"},
    {"name": "LangChain Blog", "url": "https://blog.langchain.dev/rss/"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "Andrew Chen", "url": "https://andrewchen.com/feed/"},
    {"name": "SaaStr", "url": "https://www.saastr.com/feed/"},
    {"name": "GitHub Changelog", "url": "https://github.blog/changelog/feed/"},
]

CACHE_FILE = "cache.json"
CACHE_TTL_DAYS = 21

def load_cache():
    """
    Returns {url: date_first_seen} dict.
    Migrates old format {"urls": [...]} to new format on first load,
    treating all existing URLs as seen today.
    """
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
            # Migrate old format: {"urls": [...], "last_updated": "..."}
            if "urls" in data:
                today = datetime.now().strftime("%Y-%m-%d")
                print(f"  INFO: Migrating cache.json to new format ({len(data['urls'])} entries)")
                return {url: today for url in data["urls"]}
            # New format: {"url1": "2026-04-11", ...}
            return data
    except Exception:
        pass
    return {}

def save_cache(cache):
    """Saves {url: date_first_seen} dict to cache file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2, sort_keys=True)
    except Exception as e:
        print(f"  WARNING: Cache save error: {e}")

def fetch_recent_articles(days_back=7, dry_run=False):
    cutoff = datetime.now() - timedelta(days=days_back)
    prune_cutoff = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
    today = datetime.now().strftime("%Y-%m-%d")

    cache = {} if dry_run else load_cache()
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

                # skip if seen within the last CACHE_TTL_DAYS days
                if url in cache:
                    try:
                        seen_date = datetime.strptime(cache[url], "%Y-%m-%d")
                    except ValueError:
                        seen_date = datetime.min
                    if seen_date >= prune_cutoff:
                        continue
                    # seen_date is older than TTL — treat as new (entry refreshed on save)

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

    if not dry_run:
        updated_cache = {**cache, **{a["url"]: today for a in articles}}
        save_cache(updated_cache)

    print(f"\nFetched {len(articles)} new articles from the last {days_back} days")
    return articles