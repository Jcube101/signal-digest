# Contributing to Signal Digest

Welcome. This doc explains how the project is structured, what each file does, and in what order things run. Read this before touching any code.

---

## What this project does

Signal Digest is a personal AI agent. Every Monday at 10 AM, it:
1. Fetches articles from a list of RSS sources
2. Filters and reasons over them using Claude
3. Emails a curated digest and saves a local copy

That's it. Three stages, one entry point, no web server, no database.

---

## Folder structure

```
signal_digest/
│
├── signal_digest/          # The Python package — all core logic lives here
│   ├── __init__.py         # Makes this a package; nothing interesting inside
│   ├── fetcher.py          # Stage 1: pulls RSS feeds, deduplicates via cache
│   ├── agent.py            # Stage 2: sends articles to Claude, gets digest back
│   └── deliver.py          # Stage 3: converts digest to HTML, sends email, saves archive
│
├── archive/                # Auto-created folder; stores past digests as .md files
│                           # Not committed to Git — personal content
│
├── scheduler/              # Cross-platform scheduler configs (read-only reference)
│   ├── cron.md             # How to schedule on Linux
│   ├── launchd.plist       # How to schedule on macOS
│   └── systemd/            # How to schedule on Linux with systemd
│
├── main.py                 # Entry point — the only file you ever run directly
├── run_tracker.bat         # Windows Task Scheduler trigger — calls main.py
├── cache.json              # Tracks seen article URLs with timestamps
│                           # Auto-created on first run; not committed to Git
├── .env                    # Your API key and email credentials — never committed
├── .env.example            # Template showing what goes in .env
├── CLAUDE.md               # Context file for Claude when resuming this project
├── learnings.md            # What was learned building this — agent vs script
├── spec.md                 # Architecture, sources, stack reference
└── roadmap.md              # What's done, what's next
```

---

## Execution order

When you run `python main.py`, here is exactly what happens in order:

```
main.py
  │
  ├── 1. fetcher.py → fetch_recent_articles()
  │       - Loads cache.json (seen URLs with dates)
  │       - Loops through each RSS source in SOURCES list
  │       - For each source: parses the feed, filters by date, skips cached URLs
  │       - Returns a list of article dicts: {source, title, url, summary, published}
  │       - Saves newly seen URLs to cache.json
  │
  ├── 2. agent.py → run_agent(articles)
  │       - Formats all articles into a prompt string
  │       - Sends to Claude via Anthropic API with a persona-specific system prompt
  │       - Claude filters, clusters, extracts signals, writes digest
  │       - Returns the digest as a markdown string
  │
  └── 3. deliver.py → send_digest(digest_text)
          - Saves the digest to archive/ as a dated .md file
          - Converts markdown to HTML using the markdown library
          - Sends HTML email via Gmail SMTP
          - Prints confirmation
```

---

## The files that matter most

**`signal_digest/fetcher.py`** — Start here if you want to add or change sources. The `SOURCES` list at the top is where all RSS feed URLs live. The deduplication logic reads and writes `cache.json`. If articles are being skipped unexpectedly, check the cache.

**`signal_digest/agent.py`** — This is the agent. The `SYSTEM_PROMPT` constant at the top defines the reader's lens — what counts as signal, how the digest should be written, what Claude is not allowed to do (draw on training knowledge, reference articles by number). If the digest quality is off, this is where to tune it.

**`signal_digest/deliver.py`** — Controls what the email looks like. The HTML template, the date range calculation, the sender display name, and the archive path are all here.

**`main.py`** — Wires the three stages together. Also handles the `--dry-run` flag, which runs the full pipeline without sending email or updating the cache. Use this when testing changes.

---

## How to run it

**Normal run (sends email, updates cache):**
```bash
python main.py
```

**Dry run (no email, cache untouched — use this for testing):**
```bash
python main.py --dry-run
```

---

## Environment setup

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS / Linux
pip install anthropic feedparser python-dotenv markdown
```

Copy `.env.example` to `.env` and fill in:
```
ANTHROPIC_API_KEY=your_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

For `EMAIL_PASSWORD`, generate a Gmail App Password at myaccount.google.com → Security → App Passwords. Your regular Gmail password will not work.

---

## What not to touch

- **`cache.json`** — Do not manually edit this. If you want to reset it and re-fetch all articles, delete the file. It will be recreated on the next run.
- **`.env`** — Never commit this. It contains live credentials.
- **`archive/`** — Personal digest history. Not committed to Git.
- **`run_tracker.bat`** — Only relevant on Windows. Contains a hardcoded path to the project folder. Update the path if you move the project.