# Signal Digest — Spec

## How it works

Scheduler → Fetcher → Agent → Delivery

1. **Fetcher** pulls articles from 7 RSS sources published in the last 7 days
2. **Agent** reasons over the content — filtering, clustering, and extracting signals (not summaries)
3. **Delivery** converts the digest to HTML and emails it, while saving a local markdown copy to `archive/`
4. **Scheduler** runs the whole pipeline every Monday at 10 AM via Windows Task Scheduler

The agent is not a summarizer. It makes judgment calls about what matters, clusters related signals by theme, and writes to a specific reader's context. That's what makes it an agent rather than a script.

---

## Sources

| Source | Focus |
|---|---|
| Simon Willison | Independent AI analysis |
| Lenny's Newsletter | Product thinking |
| Hacker News (100+ points) | High-signal tech news |
| Benedict Evans | Tech strategy |
| Salesforce Ben | CRM / Agentforce |
| Kyle Poyar | GTM / growth |
| The Rundown AI | Daily AI news |

---

## Project structure

```
signal-digest/
├── signal_digest/
│   ├── fetcher.py      # RSS ingestion
│   ├── agent.py        # Claude reasoning loop
│   └── deliver.py      # HTML email + archive
├── main.py             # Entry point
├── run_tracker.bat     # Windows scheduler trigger
├── CLAUDE.md           # Project context for Claude
├── spec.md             # This file — architecture and design
├── roadmap.md          # Known limitations and future work
├── learnings.md        # Agent vs script — what I learned building this
└── .env.example        # Environment variable template
```

---

## Stack

| Component | Choice |
|---|---|
| Language | Python 3.11.9 |
| LLM | Claude (`claude-opus-4-5`) via Anthropic API |
| Feed parsing | feedparser |
| Delivery | Gmail SMTP SSL |
| Scheduler | Windows Task Scheduler |
| Environment | python-dotenv |
