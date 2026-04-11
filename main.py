from signal_digest.fetcher import fetch_recent_articles
from signal_digest.agent import run_agent
from signal_digest.deliver import send_digest

articles = fetch_recent_articles()
digest = run_agent(articles)

print("\n" + "="*60)
print("WEAK SIGNAL TRACKER — WEEKLY DIGEST")
print("="*60 + "\n")
print(digest)

send_digest(digest)