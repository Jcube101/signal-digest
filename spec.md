# Signal Digest — Spec

## How it works

Scheduler → Fetcher → Agent → Delivery

1. **Fetcher** pulls articles from 12 RSS sources published in the last 7 days; skips URLs cached within the last 21 days (`cache.json`); URLs older than 21 days are treated as new again
2. **Agent** reasons over the content — filtering, clustering, extracting signals as markdown hyperlinks `[Source: signal text](url)`, constrained to only the provided articles
3. **Delivery** converts the digest to HTML via the `markdown` library; email opens with "Job's Weekly Signal Digest" heading and a dynamic date range (e.g. "April 5 – 11, 2026"); saves a local markdown copy to `archive/`
4. **Scheduler** triggers the pipeline on a recurring basis. Production runs on a Raspberry Pi 5 via systemd timer (`signal-digest.timer` + `signal-digest.service`) every Monday at 10:00 AM IST. On Windows, Task Scheduler runs `run_tracker.bat` on login; the 21-day deduplication cache ensures the digest only delivers when new content exists. Output and errors are logged to `scheduler_log.txt`. See `scheduler/` for cron (Linux) and launchd (macOS) alternatives.

The agent is not a summarizer. It makes judgment calls about what matters, clusters related signals by theme, and writes to a specific reader's context. That's what makes it an agent rather than a script.

Run `python main.py --dry-run` to test the full pipeline without updating `cache.json` or sending email. Useful for verifying all 12 sources fetch cleanly after any source change.

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
| TLDR AI | Agentic AI — daily AI news |
| LangChain Blog | Agentic AI — frameworks and tooling |
| Hugging Face Blog | Agentic AI — models and open source |
| Andrew Chen | AI PM — product and growth |
| SaaStr | RevOps — B2B SaaS / GTM strategy |
| GitHub Changelog | Builder mindset — platform and tooling updates |

---

## Project structure

```
signal-digest/
├── signal_digest/
│   ├── fetcher.py      # RSS ingestion, TTL-based deduplication (21 days)
│   ├── agent.py        # Claude reasoning loop
│   └── deliver.py      # HTML email + archive
├── scheduler/          # Cross-platform scheduler configs
│   ├── cron.md         # Linux cron setup
│   ├── launchd.plist   # macOS LaunchAgent
│   └── systemd/        # Linux systemd service + timer
├── main.py             # Entry point
├── run_tracker.bat     # Windows Task Scheduler trigger (at-login, absolute venv path, logs to scheduler_log.txt)
├── scheduler_log.txt   # stdout/stderr from scheduled runs — not committed
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
