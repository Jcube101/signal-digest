# Signal Digest — Roadmap

## Planned

- [x] Error handling — graceful failure per source (bozo feed detection + try/except)
- [x] Hallucination guard — system prompt constrained to fetched content only
- [x] Deduplication — URL cache in `cache.json`; articles already seen are skipped
- [x] HTML rendering — replaced custom regex converter with `markdown` library
- [x] Source expansion — 5 new feeds added across all lens areas
- [x] Cross-platform scheduler — cron, launchd, and systemd configs in `scheduler/`

## Longer term

- [ ] Memory — store previous digests and let the agent surface multi-week patterns
- [ ] Deduplication pruning — clear `cache.json` entries older than N weeks
- [ ] MCP integration — standardise tools across agents as the project grows
- [ ] Source expansion v2 — X/Twitter accounts, YouTube channels
- [ ] Dry-run mode — fetch and filter without sending email
