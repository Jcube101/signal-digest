# Signal Digest — Project Context for Claude

## What this project is
A personal AI agent that monitors a curated list of RSS feeds, filters articles through Job's professional lens, and delivers a weekly digest to his Gmail inbox every Monday at 10 AM IST. Digests are also saved locally to an `archive/` folder.

## Owner
Job Joseph — Principal Program Manager, Revenue Operations. AI PM identity. Builder. Portfolio at job-joseph.com, GitHub at Jcube101.

## Project location
`C:\Users\jobjo\Github\signal-digest`

## Stack
- **Language**: Python 3.11.9
- **LLM**: Claude via Anthropic API (`claude-opus-4-5`)
- **Libraries**: `anthropic`, `feedparser`, `python-dotenv`
- **Delivery**: Gmail via SMTP SSL
- **Scheduler**: Windows Task Scheduler → `run_tracker.bat`
- **Environment**: `.env` file with `ANTHROPIC_API_KEY`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD`

## Project structure
```
signal-digest/
├── signal_digest/
│   ├── __init__.py
│   ├── fetcher.py       # pulls RSS feeds, filters by date
│   ├── agent.py         # Claude reasoning loop — the actual agent
│   └── deliver.py       # HTML email + local archive
├── archive/             # weekly digests saved as markdown
├── main.py              # entry point
├── run_tracker.bat      # Windows Task Scheduler trigger
├── .env                 # API key + email credentials (not committed)
├── CLAUDE.md            # this file
└── learnings.md         # explanation of agent vs script, architecture
```

## How it works
1. `fetcher.py` pulls articles from 7 RSS sources published in the last 7 days
2. `agent.py` sends all articles to Claude with a persona-specific system prompt
3. Claude filters ruthlessly, extracts signals (not summaries), clusters by theme, writes digest
4. `deliver.py` converts markdown to HTML, emails it, saves a `.md` copy to `archive/`
5. Windows Task Scheduler runs `run_tracker.bat` every Monday at 10 AM IST

## RSS Sources (defined in fetcher.py)
| Name | Focus |
|---|---|
| Simon Willison | Independent AI analysis |
| Lenny's Newsletter | Product thinking |
| Hacker News (100+ points) | High-signal tech news |
| Benedict Evans | Tech strategy |
| Salesforce Ben | CRM / Agentforce |
| Kyle Poyar | GTM / growth |
| The Rundown AI | Daily AI news |

## Job's lens (defined in agent.py system prompt)
- Agentic AI — how agents are built, where they're heading
- AI PM thinking — product decisions, AI-native workflows
- RevOps automation — GTM tooling, CRM intelligence
- Builder mindset — tools, frameworks, open source

## Known limitations / future work
- [ ] Deduplication — skip articles already seen in previous weeks (URL cache in `.json`)
- [ ] Error handling — wrap each RSS fetch in try/except so one bad feed doesn't crash the run
- [ ] HTML rendering — markdown-to-HTML is a lightweight custom converter; could be replaced with `markdown` library for robustness
- [ ] Source expansion — X/Twitter accounts, YouTube channels (harder, v2)
- [ ] Agent hallucination guard — agent occasionally draws on training knowledge, not just fetched articles. Need to tighten prompt to reason only over provided content.

## Environment setup (fresh machine)
```bash
python -m venv venv
venv\Scripts\activate
pip install anthropic feedparser python-dotenv
```
Add `.env` with:
```
ANTHROPIC_API_KEY=your_key
EMAIL_ADDRESS=your_gmail
EMAIL_PASSWORD=your_app_password
```
