# Signal Digest — systemd Setup (Linux)

## Setup

1. Edit `signal-digest.service` — replace `YOUR_USERNAME` with your Linux username.

2. Copy both files to your systemd user directory:
   ```bash
   mkdir -p ~/.config/systemd/user
   cp signal-digest.service signal-digest.timer ~/.config/systemd/user/
   ```

3. Reload systemd and enable the timer:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable signal-digest.timer
   systemctl --user start signal-digest.timer
   ```

4. Verify the timer is active:
   ```bash
   systemctl --user list-timers signal-digest.timer
   ```

## View logs

```bash
journalctl --user -u signal-digest.service
```

## Run manually

```bash
systemctl --user start signal-digest.service
```
