# Signal Digest — Roadmap

## Planned

- [ ] Deduplication — skip articles seen in previous weeks (URL cache in `.json`)
- [ ] Error handling — wrap each RSS fetch in try/except so one bad feed doesn't crash the run
- [ ] Hallucination guard — tighten system prompt to constrain agent to fetched content only
- [ ] HTML rendering — replace lightweight custom converter with `markdown` library for robustness
- [ ] Source expansion — add more feeds per lens area
- [ ] Cross-platform scheduler — alternatives to Windows Task Scheduler (cron, launchd)

## Longer term

- [ ] Memory — store previous digests and let the agent surface multi-week patterns
- [ ] Deduplication across weeks — never surface the same article twice
- [ ] MCP integration — standardise tools across agents as the project grows
- [ ] Source expansion v2 — X/Twitter accounts, YouTube channels
