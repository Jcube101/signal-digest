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
- **Libraries**: `anthropic`, `feedparser`, `python-dotenv`, `markdown`
- **Delivery**: Gmail via SMTP SSL
- **Scheduler**: Windows Task Scheduler → `run_tracker.bat` (cron/launchd/systemd configs also in `scheduler/`)
- **Environment**: `.env` file with `ANTHROPIC_API_KEY`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD`

## Project structure
```
signal-digest/
├── signal_digest/
│   ├── __init__.py
│   ├── fetcher.py       # pulls RSS feeds, filters by date, deduplicates via cache.json
│   ├── agent.py         # Claude reasoning loop — the actual agent
│   └── deliver.py       # HTML email (via markdown library) + local archive
├── scheduler/           # cross-platform scheduler configs
│   ├── cron.md          # Linux cron setup
│   ├── launchd.plist    # macOS LaunchAgent
│   └── systemd/         # Linux systemd service + timer
├── archive/             # weekly digests saved as markdown
├── main.py              # entry point
├── run_tracker.bat      # Windows Task Scheduler trigger
├── .env                 # API key + email credentials (not committed)
├── cache.json           # seen article URLs — prevents re-surfacing (not committed)
├── CLAUDE.md            # this file
├── spec.md              # architecture, sources, stack
├── roadmap.md           # what's done and what's next
└── learnings.md         # explanation of agent vs script, architecture
```

## How it works
1. `fetcher.py` pulls articles from 12 RSS sources published in the last 7 days, skipping any URLs already in `cache.json`
2. `agent.py` sends all new articles to Claude with a persona-specific system prompt
3. Claude filters ruthlessly, extracts signals (not summaries), clusters by theme, writes digest — constrained to only reason over the provided articles
4. `deliver.py` converts markdown to HTML via the `markdown` library, emails it, saves a `.md` copy to `archive/`
5. Windows Task Scheduler runs `run_tracker.bat` every Monday at 10 AM IST (Linux/macOS configs in `scheduler/`)

## RSS Sources (defined in fetcher.py)
| Name | Lens area |
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

## Job's lens (defined in agent.py system prompt)
- Agentic AI — how agents are built, where they're heading
- AI PM thinking — product decisions, AI-native workflows
- RevOps automation — GTM tooling, CRM intelligence
- Builder mindset — tools, frameworks, open source

## Known limitations / future work
- [ ] Memory — store previous digests and let the agent surface multi-week patterns
- [ ] Deduplication pruning — clear `cache.json` entries older than N weeks
- [ ] MCP integration — standardise tools as the project grows
- [ ] Source expansion v2 — X/Twitter accounts, YouTube channels

## Environment setup (fresh machine)
```bash
python -m venv venv
venv\Scripts\activate
pip install anthropic feedparser python-dotenv markdown
```
Add `.env` with:
```
ANTHROPIC_API_KEY=your_key
EMAIL_ADDRESS=your_gmail
EMAIL_PASSWORD=your_app_password
```
