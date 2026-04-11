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

| Source | Lens area |
|---|---|
| Simon Willison | Agentic AI — independent analysis |
| Lenny's Newsletter | AI PM — product thinking |
| Hacker News (100+ points) | Builder mindset — high-signal tech news |
| Benedict Evans | AI PM — tech strategy |
| Salesforce Ben | RevOps — CRM / Agentforce |
| Kyle Poyar | RevOps — GTM / growth |
| The Rundown AI | Agentic AI — daily AI news |
| LangChain Blog | Agentic AI — frameworks and tooling |
| Hugging Face Blog | Agentic AI — models and open source |
| Andrew Chen | AI PM — product and growth |
| OpenView Partners | RevOps — B2B GTM strategy |
| GitHub Changelog | Builder mindset — platform and tooling updates |

---

## Project structure

```
signal-digest/
├── signal_digest/
│   ├── fetcher.py      # RSS ingestion, deduplication
│   ├── agent.py        # Claude reasoning loop
│   └── deliver.py      # HTML email + archive
├── scheduler/          # Cross-platform scheduler configs
│   ├── cron.md         # Linux cron setup
│   ├── launchd.plist   # macOS LaunchAgent
│   └── systemd/        # Linux systemd service + timer
├── main.py             # Entry point
├── run_tracker.bat     # Windows Task Scheduler trigger
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
| Markdown rendering | markdown (with `extra` + `nl2br` extensions) |
| Delivery | Gmail SMTP SSL |
| Scheduler | Windows Task Scheduler / cron / launchd / systemd |
| Environment | python-dotenv |
