# Signal Digest — Linux Cron Setup

## Schedule

Add this line to your crontab (`crontab -e`):

```
0 10 * * 1 cd /path/to/signal-digest && venv/bin/python main.py >> logs/signal_digest.log 2>&1
```

Replace `/path/to/signal-digest` with the absolute path to your project.

## Steps

1. Create the logs directory:
   ```bash
   mkdir -p /path/to/signal-digest/logs
   ```

2. Open crontab editor:
   ```bash
   crontab -e
   ```

3. Add the line above, then save and exit.

4. Verify the job is registered:
   ```bash
   crontab -l
   ```

## Notes

- The cron expression `0 10 * * 1` means "10:00 AM every Monday".
- Cron uses the system timezone. Adjust the hour if you need a specific timezone.
- Logs accumulate in `logs/signal_digest.log` — rotate or clear periodically.
- Make sure the venv Python has all dependencies installed (`pip install anthropic feedparser python-dotenv markdown`).
