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

Test without sending email or updating the cache:

```bash
python main.py --dry-run
```

---

## Scheduling

### Linux / Raspberry Pi (systemd timer)

The recommended production setup uses systemd. Config files are in `scheduler/systemd/`:

1. Edit `signal-digest.service` and `signal-digest.timer` to set your project path
2. Copy both files to `~/.config/systemd/user/`
3. Enable and start the timer:

```bash
systemctl --user enable signal-digest.timer
systemctl --user start signal-digest.timer
```

The timer runs every Monday at 10:00 AM (local time). Check status with `systemctl --user status signal-digest.timer`.

See `scheduler/` for alternative Linux (cron) and macOS (launchd) configs.

### Windows (Task Scheduler)

Use Task Scheduler to run `run_tracker.bat` on a weekly schedule. Set the trigger to your preferred day and time. Ensure the machine is plugged in and not set to sleep during the scheduled run.

---

## Docs

- [spec.md](spec.md) — architecture, sources, stack, project structure
- [roadmap.md](roadmap.md) — known limitations and future work
- [learnings.md](learnings.md) — what I learned building this

---

## Author

Job Joseph — Principal Program Manager, Revenue Operations. Building AI-powered tools at the intersection of product thinking and automation.

[Portfolio](https://job-joseph.com) · [LinkedIn](https://linkedin.com/in/job-joseph) · [GitHub](https://github.com/Jcube101)
