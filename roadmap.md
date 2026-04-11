# Signal Digest — Roadmap

## Planned

- [x] Error handling — graceful failure per source (bozo feed detection + try/except)
- [x] Hallucination guard — system prompt constrained to fetched content only
- [x] Deduplication — URL cache in `cache.json` with 21-day TTL; articles re-surface after expiry
- [x] HTML rendering — replaced custom regex converter with `markdown` library
- [x] Source expansion — 5 new feeds added across all lens areas; broken sources replaced
- [x] Cross-platform scheduler — cron, launchd, and systemd configs in `scheduler/`
- [x] Signal hyperlinks — every signal formatted as `[Source: text](url)`; article numbers banned
- [x] Email polish — "Job's Weekly Signal Digest" heading, dynamic date range subtitle, "Signal Digest" sender display name
- [x] Dry-run mode — `python main.py --dry-run` tests full pipeline without touching cache or sending email
- [x] Deduplication pruning — cache entries expire after 21 days; articles re-surface automatically

## Longer term

- [ ] Memory — store previous digests and let the agent surface multi-week patterns
- [ ] MCP integration — standardise tools across agents as the project grows
- [ ] Source expansion v2 — X/Twitter accounts, YouTube channels
