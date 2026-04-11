# Signal Digest

A personal AI agent that monitors curated RSS sources, filters content through a defined lens, and delivers a weekly digest to your inbox every Monday.

Built as a learning project to understand the difference between scripting and agentic reasoning.

---

## Quick start

**Prerequisites:** Python 3.9+, Gmail account, Anthropic API key

```bash
git clone https://github.com/Jcube101/signal-digest.git
cd signal-digest
python -m venv venv
venv\Scripts\activate        # Windows
pip install anthropic feedparser python-dotenv markdown
```

Copy `.env.example` to `.env` and fill in your credentials:

```
ANTHROPIC_API_KEY=your_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

For `EMAIL_PASSWORD`, generate a Gmail App Password at myaccount.google.com → Security → App Passwords.

Run manually:

```bash
python main.py
```

---

## Scheduling (Windows)

Use Windows Task Scheduler to run `run_tracker.bat` on a weekly schedule. Set trigger to your preferred day and time. Ensure the machine is plugged in and not set to sleep during the scheduled run.

---

## Docs

- [spec.md](spec.md) — architecture, sources, stack, project structure
- [roadmap.md](roadmap.md) — known limitations and future work
- [learnings.md](learnings.md) — what I learned building this

---

## Author

Job Joseph — Principal Program Manager, Revenue Operations. Building AI-powered tools at the intersection of product thinking and automation.

[Portfolio](https://job-joseph.com) · [LinkedIn](https://linkedin.com/in/job-joseph) · [GitHub](https://github.com/Jcube101)
