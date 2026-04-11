# Signal Digest

A personal AI agent that monitors curated RSS sources, filters content through a defined lens, and delivers a weekly digest to your inbox every Monday.

Built as a learning project to understand the difference between scripting and agentic reasoning.

---

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

## Setup

**Prerequisites:** Python 3.9+, Gmail account, Anthropic API key

```bash
git clone https://github.com/Jcube101/signal-digest.git
cd signal-digest
python -m venv venv
venv\Scripts\activate        # Windows
pip install anthropic feedparser python-dotenv
```

Copy `.env.example` to `.env` and fill in your credentials:
ANTHROPIC_API_KEY=your_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

For `EMAIL_PASSWORD`, generate a Gmail App Password at myaccount.google.com → Security → App Passwords.

Run manually:
```bash
python main.py
```

---

## Scheduling (Windows)

Use Windows Task Scheduler to run `run_tracker.bat` on a weekly schedule. Set trigger to your preferred day and time. Ensure the machine is plugged in and not set to sleep during the scheduled run.

---

## Project structure
signal-digest/
├── signal_digest/
│   ├── fetcher.py      # RSS ingestion
│   ├── agent.py        # Claude reasoning loop
│   └── deliver.py      # HTML email + archive
├── main.py             # Entry point
├── run_tracker.bat     # Windows scheduler trigger
├── CLAUDE.md           # Project context for Claude
├── learnings.md        # Agent vs script — what I learned building this
└── .env.example        # Environment variable template

---

## Stack

- **LLM:** Claude (`claude-opus-4-5`) via Anthropic API
- **Feed parsing:** feedparser
- **Delivery:** Gmail SMTP
- **Scheduler:** Windows Task Scheduler

---

## Roadmap

- [ ] Deduplication — skip articles seen in previous weeks
- [ ] Error handling — graceful failure per source
- [ ] Hallucination guard — constrain agent to fetched content only
- [ ] Source expansion — add more feeds per lens area
- [ ] Cross-platform scheduler support

---

## Author

Job Joseph — Principal Program Manager, Revenue Operations. Building AI-powered tools at the intersection of product thinking and automation.

[Portfolio](https://job-joseph.com)
[LinkedIn](https://linkedin.com/in/job-joseph)
[GitHub](https://github.com/Jcube101)