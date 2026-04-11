import sys
from signal_digest.fetcher import fetch_recent_articles
from signal_digest.agent import run_agent
from signal_digest.deliver import send_digest

try:
    articles = fetch_recent_articles()
    digest = run_agent(articles)

    print("\n" + "="*60)
    print("SIGNAL DIGEST — WEEKLY DIGEST")
    print("="*60 + "\n")
    print(digest)

    send_digest(digest)
    sys.exit(0)

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    sys.exit(1)
